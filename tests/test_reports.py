import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

grade = module('grader', 'evals/grade.py')
package = module('package', 'scripts/build_skill.py')


def synthetic(scenario='full'):
    """Synthetic TOOLING fixture, not model performance evidence."""
    fixture = json.loads((ROOT/'evals/expected.json').read_text())[scenario]
    report = {'schema_version': '1.0', 'scope': {'read': fixture['read'], 'unread': fixture['unread'], 'reading_order': fixture['read']+fixture['unread'], 'limitations': ['Synthetic tooling fixture.'], 'preservation': 'not_hash_verified'}, 'ledger': [], 'findings': []}
    for i, case in enumerate(fixture['cases']):
        evidence = []
        for a in case['anchors']:
            if 'any_of' in a: a = a['any_of'][0]
            lines = (ROOT/a['path']).read_text().splitlines()
            n = next(n for n,line in enumerate(lines,1) if a['text'] in line)
            evidence.append(dict(path=a['path'], chapter=lines[0][2:], line_start=n, line_end=n, quote=lines[n-1]))
        fid = 'F'+str(i)
        report['ledger'].append(dict(id=fid, entity=case['id'], fact='Synthetic fact.', story_time='sample', certainty='explicit', evidence=evidence))
        report['findings'].append(dict(id='I'+str(i), classification=case['classification'], confidence='high', title=case['id'], fact_ids=[fid], evidence=copy.deepcopy(evidence), reasoning='Synthetic reasoning.', repair='Synthetic proposal.'))
    return report


class ReportTests(unittest.TestCase):
    def setUp(self): self.report = synthetic()
    def rejects(self): self.assertTrue(grade.grade(self.report, 'full'))
    def test_full_and_prefix(self):
        for scenario in ('full','prefix'):
            self.assertEqual([], grade.grade(synthetic(scenario),scenario))
    def test_wrong_quote(self):
        self.report['findings'][0]['evidence'][0]['quote']='Invented'
        self.rejects()
    def test_wrong_lines(self):
        self.report['findings'][0]['evidence'][0]['line_end']=999
        self.rejects()
    def test_boolean_line(self):
        self.report['findings'][0]['evidence'][0]['line_start']=True
        self.rejects()
    def test_unread_leak(self):
        report=synthetic('prefix')
        report['findings'][0]['evidence'][0]['path']='examples/manuscript/04.md'
        self.assertTrue(grade.grade(report,'prefix'))
    def test_path_traversal(self):
        self.report['findings'][0]['evidence'][0]['path']='../outside.md'
        self.rejects()
    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'root'; root.mkdir()
            (Path(tmp)/'outside.md').write_text('outside')
            (root/'inside.md').symlink_to(Path(tmp)/'outside.md')
            report={'schema_version':'1.0','scope':{'read':['inside.md'],'unread':[],'reading_order':['inside.md'],'limitations':[],'preservation':'not_hash_verified'},'ledger':[dict(id='F1',entity='x',fact='x',story_time='x',certainty='explicit',evidence=[dict(path='inside.md',chapter='x',line_start=1,line_end=1,quote='outside')])],'findings':[]}
            self.assertTrue(grade.validate(report,root))
    def test_duplicate_issue(self):
        issue=copy.deepcopy(self.report['findings'][0]); issue['id']='I99'
        self.report['findings'].append(issue); self.rejects()
    def test_duplicate_evidence(self):
        evidence=self.report['findings'][0]['evidence']; evidence.append(copy.deepcopy(evidence[0])); self.rejects()
    def test_missing_issue(self):
        self.report['findings'].pop(0); self.rejects()
    def test_wrong_classification(self):
        self.report['findings'][0]['classification']='author_question'; self.rejects()
    def test_unexpected_contradiction(self):
        issue=copy.deepcopy(self.report['findings'][3]); issue.update(id='I99',classification='contradiction')
        self.report['findings'].append(issue); self.rejects()
    def test_unknown_fact(self):
        self.report['findings'][0]['fact_ids']=['MISSING']; self.rejects()
    def test_false_hash_claim(self):
        self.report['scope']['preservation']='hash_verified_unchanged'; self.rejects()
    def test_equal_and_unequal_hashes(self):
        self.report['scope']['preservation']='hash_verified_unchanged'
        self.report['scope']['hashes']=[dict(path=p,before=hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),after=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in self.report['scope']['read']]
        self.assertEqual([],grade.validate(self.report))
        self.report['scope']['hashes'][0]['after']='0'*64; self.rejects()
    def test_malformed_top_level(self):
        for value in (None,[],'text',{'scope':None}): self.assertTrue(grade.validate(value))
    def test_curated_example(self):
        self.assertEqual([],grade.validate(json.loads((ROOT/'examples/yakuza/curated-report.json').read_text())))
    def test_saved_behavioral_outcomes(self):
        folder=ROOT/'evals/baselines/2026-10-23'
        full=json.loads((folder/'full.json').read_text())
        prefix=json.loads((folder/'prefix.json').read_text())
        self.assertEqual([],grade.grade(full,'full'))
        self.assertEqual([],grade.validate(prefix))
        self.assertEqual(['Expected exactly one match for bell; got 0.'],grade.grade(prefix,'prefix'))

    def test_prefix_uncertainty_requires_author_question(self):
        """Keep the known prefix miss explicit: uncertainty is not a finding."""
        folder=ROOT/'evals/baselines/2026-10-23'
        prefix=json.loads((folder/'prefix.json').read_text())
        bell_text='might have dreamed it'
        bell_evidence=[e for e in prefix['ledger'] if e['entity'] == 'Tess / tower bell'][0]['evidence']
        self.assertTrue(any(bell_text in e['quote'] for e in bell_evidence))
        self.assertFalse(any(f['classification'] == 'author_question' and any(bell_text in e['quote'] for e in f['evidence']) for f in prefix['findings']))
        self.assertEqual(['Expected exactly one match for bell; got 0.'], grade.grade(prefix, 'prefix'))

    def test_updated_prefix_detects_uncertainty_question(self):
        folder=ROOT/'evals/baselines/2026-10-27'
        prefix=json.loads((folder/'prefix.json').read_text())
        self.assertEqual([], grade.grade(prefix, 'prefix'))
        bell=[f for f in prefix['findings'] if f['classification'] == 'author_question' and any('might have dreamed it' in e['quote'] for e in f['evidence'])]
        self.assertEqual(1, len(bell))
        hashes=json.loads((folder/'prefix-hashes.json').read_text())
        self.assertEqual(hashes['before'], hashes['after'])
        for path, digest in hashes['after'].items():
            self.assertEqual(digest, hashlib.sha256((ROOT/path).read_bytes()).hexdigest())
    def test_saved_source_hashes(self):
        for name in ('full','prefix'):
            report=json.loads((ROOT/f'evals/baselines/2026-10-23/{name}.json').read_text())
            for entry in report['scope']['hashes']:
                self.assertEqual(entry['before'],entry['after'])
                self.assertEqual(entry['after'],hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest())


class PackageTests(unittest.TestCase):
    def test_archive_is_deterministic_and_skill_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=package.build(Path(tmp)/'a.zip'); b=package.build(Path(tmp)/'b.zip')
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with zipfile.ZipFile(a) as archive:
                names=archive.namelist()
                self.assertIn('storyera/SKILL.md',names); self.assertIn('storyera/LICENSE',names)
                self.assertTrue(all(n.startswith('storyera/') for n in names))
                self.assertFalse(any('yakuza' in n or 'evals' in n for n in names))
    def test_skill_frontmatter_and_references(self):
        text=(ROOT/'skills/storyera/SKILL.md').read_text()
        self.assertTrue(text.startswith('---\nname: storyera\n')); self.assertNotIn('[TODO:',text)
        self.assertIn('A ledger entry alone does not surface the canon decision',text)
        for target in re.findall(r'\]\((references/[^)]+)\)',text):
            self.assertTrue((ROOT/'skills/storyera'/target).is_file())
        self.assertEqual((ROOT/'skills/storyera/LICENSE').read_text().strip(),(ROOT/'LICENSE').read_text().split('Scope exception:')[0].strip())
    def test_documentation_local_links(self):
        for path in ROOT.rglob('*.md'):
            text=re.sub(r'```.*?```','',path.read_text(),flags=re.S)
            targets=re.findall(r'\]\(([^)]+)\)',text)+re.findall(r'src="([^"]+)"',text)
            for target in targets:
                if '://' in target or target.startswith('#'): continue
                self.assertTrue((path.parent/target.split('#')[0]).exists(),f'{path}: {target}')
    def test_excerpt_provenance(self):
        provenance=json.loads((ROOT/'examples/yakuza/provenance.json').read_text()); excerpt=(ROOT/'examples/yakuza/excerpts.md').read_text()
        self.assertEqual(64,len(provenance['source_sha256']))
        for record in provenance['excerpts']:
            self.assertIn(record['quote'],excerpt); self.assertGreater(record['original_line_start'],0)
    def test_no_full_manuscript_or_local_paths(self):
        for path in ROOT.rglob('*'):
            if path.is_file() and '.git' not in path.parts and path.suffix in ('.md','.json','.py','.yaml','.yml'):
                self.assertNotIn('/Users/'+'mohamedansar',path.read_text(),str(path))
                self.assertNotEqual(path.name,'YAKUZA_The_Borrowed_Life.md')
