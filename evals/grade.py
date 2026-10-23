#!/usr/bin/env python3
"""Offline report/evidence checks. Does not call a model or audit a novel."""
import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re

LABELS = {"contradiction", "explained_change", "intentional_mystery", "author_question"}
CONFIDENCE = {"high", "medium", "low"}
CERTAINTY = {"explicit", "character_claim", "inference"}
ROOT = Path(__file__).resolve().parents[1]


def validate(report, root=ROOT):
    """Return errors; reject malformed structure before checking source evidence."""
    errors = []

    def fail(message):
        errors.append(message)

    def strings(value):
        return isinstance(value, list) and all(isinstance(x, str) and x for x in value)

    def safe_path(value):
        if not isinstance(value, str) or not value or "\\" in value:
            return False
        p = PurePosixPath(value)
        return not p.is_absolute() and ".." not in p.parts and str(p) == value

    if not isinstance(report, dict):
        return ["Report must be an object."]
    if report.get("schema_version") != "1.0":
        fail("schema_version must be 1.0.")
    scope = report.get("scope")
    if not isinstance(scope, dict):
        return errors + ["scope must be an object."]
    for key in ("read", "unread", "reading_order", "limitations"):
        if not strings(scope.get(key)):
            fail("scope.%s must be a list of nonempty strings." % key)
    if errors:
        return errors
    read, unread, order = (scope[k] for k in ("read", "unread", "reading_order"))
    for key, paths in (("read", read), ("unread", unread), ("reading_order", order)):
        if len(paths) != len(set(paths)) or not all(safe_path(p) for p in paths):
            fail("scope.%s has duplicate or unsafe paths." % key)
    if set(read) & set(unread) or set(order) != set(read + unread):
        fail("Scope must partition reading_order into disjoint read and unread files.")
    preservation = scope.get("preservation")
    if preservation not in ("hash_verified_unchanged", "not_hash_verified", "changed"):
        fail("Invalid preservation status.")
    if preservation == "hash_verified_unchanged":
        hashes = scope.get("hashes")
        if not isinstance(hashes, list):
            fail("Hash-verified status requires hashes.")
        else:
            paths = []
            for entry in hashes:
                if not isinstance(entry, dict):
                    fail("Malformed hash entry.")
                    continue
                paths.append(entry.get("path"))
                before, after = entry.get("before"), entry.get("after")
                if not isinstance(before, str) or not re.fullmatch(r"[0-9a-f]{64}", before) or before != after:
                    fail("Missing or unequal SHA-256 values.")
            if Counter(str(p) for p in paths) != Counter(read):
                fail("Hashes must cover each read file once.")

    def evidence(entries, context):
        if not isinstance(entries, list) or not entries:
            fail(context + ": evidence must be nonempty.")
            return
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict):
                fail(context + ": evidence entry must be an object.")
                continue
            path = entry.get("path")
            start, end = entry.get("line_start"), entry.get("line_end")
            quote = entry.get("quote")
            if not safe_path(path) or path not in read:
                fail(context + ": evidence path must be safe and reviewed.")
                continue
            if not isinstance(entry.get("chapter"), str) or not entry["chapter"]:
                fail(context + ": missing chapter.")
            if type(start) is not int or type(end) is not int or start < 1 or end < start:
                fail(context + ": invalid line range.")
                continue
            key = (path, start, end)
            if key in seen:
                fail(context + ": duplicate evidence.")
            seen.add(key)
            target = (Path(root) / path).resolve()
            try:
                target.relative_to(Path(root).resolve())
            except ValueError:
                fail(context + ": evidence escapes source root.")
                continue
            try:
                lines = target.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError):
                fail(context + ": evidence source unavailable.")
                continue
            if end > len(lines) or not isinstance(quote, str) or quote != "\n".join(lines[start - 1:end]):
                fail(context + ": quote or line range does not match source.")

    ledger, findings = report.get("ledger"), report.get("findings")
    if not isinstance(ledger, list) or not isinstance(findings, list):
        return errors + ["ledger and findings must be lists."]
    fact_ids, finding_ids = set(), set()
    for fact in ledger:
        if not isinstance(fact, dict):
            fail("Ledger entry must be an object.")
            continue
        for key in ("id", "entity", "fact", "story_time"):
            if not isinstance(fact.get(key), str) or not fact[key].strip():
                fail("Ledger missing text field: " + key)
        ident = fact.get("id")
        if isinstance(ident, str):
            if ident in fact_ids:
                fail("Duplicate fact ID.")
            fact_ids.add(ident)
        if not isinstance(fact.get("certainty"), str) or fact["certainty"] not in CERTAINTY:
            fail("Invalid fact certainty.")
        evidence(fact.get("evidence"), "Ledger " + str(ident))
    for finding in findings:
        if not isinstance(finding, dict):
            fail("Finding must be an object.")
            continue
        for key in ("id", "title", "reasoning", "repair"):
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                fail("Finding missing text field: " + key)
        ident = finding.get("id")
        if isinstance(ident, str):
            if ident in finding_ids:
                fail("Duplicate finding ID.")
            finding_ids.add(ident)
        if not isinstance(finding.get("classification"), str) or finding["classification"] not in LABELS or not isinstance(finding.get("confidence"), str) or finding["confidence"] not in CONFIDENCE:
            fail("Invalid classification or confidence.")
        refs = finding.get("fact_ids")
        if not strings(refs) or not refs or not set(refs).issubset(fact_ids) or len(refs) != len(set(refs)):
            fail("Finding must reference existing, distinct fact IDs.")
        evidence(finding.get("evidence"), "Finding " + str(ident))
        if finding.get("classification") == "contradiction" and isinstance(finding.get("evidence"), list) and len(finding["evidence"]) < 2:
            fail("A contradiction requires paired evidence.")
    return errors


def grade(report, scenario, root=ROOT, fixture_path=None):
    errors = validate(report, root)
    if errors:
        return errors
    fixtures = json.loads(Path(fixture_path or ROOT / "evals/expected.json").read_text())
    expected = fixtures[scenario]
    if report["scope"]["read"] != expected["read"] or report["scope"]["unread"] != expected["unread"] or report["scope"]["reading_order"] != expected["read"] + expected["unread"]:
        errors.append("Scope/order differs from scenario.")
    matched = Counter()
    def anchor_matches(anchor, evidence):
        if "any_of" in anchor:
            return any(anchor_matches(choice, evidence) for choice in anchor["any_of"])
        return any(anchor["path"] == e["path"] and anchor["text"] in e["quote"] for e in evidence)
    for finding in report["findings"]:
        evidence = finding["evidence"]
        if any(e["line_end"] - e["line_start"] > 2 for e in evidence):
            errors.append("Fixture citations may span at most three lines.")
        matches = []
        for case in expected["cases"]:
            if finding["classification"] == case["classification"] and all(anchor_matches(a, evidence) for a in case["anchors"]):
                matches.append(case["id"])
        if len(matches) > 1:
            errors.append("One finding conflates multiple seeded cases.")
        for ident in matches:
            matched[ident] += 1
        if finding["classification"] == "contradiction" and not matches:
            errors.append("Unexpected or incorrectly evidenced contradiction: " + finding["id"])
    for case in expected["cases"]:
        if matched[case["id"]] != 1:
            errors.append("Expected exactly one match for %s; got %s." % (case["id"], matched[case["id"]]))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--scenario", choices=("full", "prefix"))
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        errors = grade(report, args.scenario, args.root) if args.scenario else validate(report, args.root)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = ["Unable to validate report: " + str(exc)]
    for error in errors:
        print("FAIL: " + error)
    if not errors:
        print("PASS: contract and source evidence" + ("; scenario " + args.scenario if args.scenario else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
