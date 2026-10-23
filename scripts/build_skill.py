#!/usr/bin/env python3
"""Build a deterministic folder ZIP; never bundle manuscripts or eval keys."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(output):
    source = ROOT / "skills/storyera"
    output = Path(output).resolve()
    if source.resolve() in output.parents:
        raise ValueError("Output must be outside the skill folder.")
    files = sorted(p for p in source.rglob("*") if p.is_file())
    if any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("Refusing symlinks in portable package.")
    if not (source / "SKILL.md").is_file() or not (source / "LICENSE").is_file():
        raise ValueError("Skill entrypoint or standalone license missing.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            if "__pycache__" in path.parts or path.name.startswith("."):
                continue
            info = zipfile.ZipInfo("storyera/" + str(path.relative_to(source)), date_time=(2026, 10, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    print(build(parser.parse_args().output))
