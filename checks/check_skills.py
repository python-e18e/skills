"""Check plugin discovery and offline matching with only the standard library."""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
assert marketplace["name"] == "python-e18e"
assert marketplace["owner"]["name"]
assert marketplace["plugins"]

for entry in marketplace["plugins"]:
    plugin_root = (ROOT / entry["source"]).resolve()
    assert plugin_root.is_relative_to(ROOT)
    plugin = json.loads((plugin_root / ".claude-plugin/plugin.json").read_text())
    assert plugin["name"] == entry["name"]
    assert plugin["version"] == marketplace["metadata"]["version"]
    skills = list((plugin_root / "skills").glob("*/SKILL.md"))
    assert skills, "Plugin must contain discoverable skills"
    for skill in skills:
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill.read_text(), re.S)
        assert frontmatter, f"Missing frontmatter: {skill}"
        fields = dict(line.split(": ", 1) for line in frontmatter[1].splitlines())
        assert fields["name"] == skill.parent.name
        assert fields["description"].strip()

skill_dir = ROOT / "skills/module-replacements"
catalog = json.loads((skill_dir / "replacements.json").read_text())
assert catalog
for record in catalog:
    for field in ("name", "alternative", "minimum_python", "kind", "compatibility", "guidance", "source"):
        assert isinstance(record[field], str) and record[field].strip()
    assert record["kind"] in {"stdlib", "package", "stdlib-or-package"}
    assert record["compatibility"] in {"drop-in", "import-only", "conditional", "code-change"}
    assert isinstance(record["references"], list)
    assert all(url.startswith("https://") for url in [record["source"], *record["references"]])

with tempfile.TemporaryDirectory() as cwd:
    command = [sys.executable, str(skill_dir / "match.py")]
    # Match from outside the checkout, preserving the catalog's full guidance.
    result = subprocess.run(command + [record["name"] for record in catalog], cwd=cwd, text=True, capture_output=True, check=True)
    assert json.loads(result.stdout) == catalog, "Catalog names must be unique after normalization"
    result = subprocess.run(command + ["Backports__ZoneInfo", "backports.zoneinfo", "PyPDF2", "not-in-catalog"], cwd=cwd, text=True, capture_output=True, check=True)
    assert json.loads(result.stdout) == [next(r for r in catalog if r["name"] == name) for name in ("backports.zoneinfo", "PyPDF2")]
    result = subprocess.run(command + ["not-in-catalog"], cwd=cwd, text=True, capture_output=True, check=True)
    assert json.loads(result.stdout) == []
    for args in ([], ["tomli>=2"], ["requests[security]"], ["tomli; python_version < '3.11'"], ["../tomli"], ["tömli"], ["tomli-"]):
        result = subprocess.run(command + args, cwd=cwd, text=True, capture_output=True)
        assert result.returncode == 2 and not result.stdout, args

print(f"Plugin, skills, and offline matcher valid ({len(catalog)} catalog entries).")
