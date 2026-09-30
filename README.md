# python-e18e/skills

Python ecosystem modernization skills, distributed as a Claude Code plugin
marketplace. Follows the structure of [e18e/skills](https://github.com/e18e/skills)
with Python-specific guidance and a standard-library matcher.

## Install (Claude Code)

```text
/plugin marketplace add python-e18e/skills
/plugin install skills@python-e18e
```

Ask for a Python dependency audit, or invoke `/skills:module-replacements`.
See [Claude's marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).
Other agents that support `SKILL.md` can use the
[`skills/module-replacements`](skills/module-replacements) folder directly;
keep its matcher and catalog together.

## Included skill

[`module-replacements`](skills/module-replacements/SKILL.md) finds dependencies
with standard-library or maintained alternatives, explains compatibility and
Python version limits, and applies migrations within the user's requested scope.
It includes an offline snapshot of the separate
[replacement catalog](https://github.com/python-e18e/module-replacements).
The skill does not require the CLI, codemods, or MCP server.

Python 3.11+ is required for the matcher and checks. No dependencies or package
installation are needed:

```sh
python skills/module-replacements/match.py tomli appdirs backports.zoneinfo
python checks/check_skills.py
claude plugin validate .
```

The matcher takes distribution names, not import names or requirement strings.
It emits full catalog entries as JSON, deduplicated in input order; no matches
produce `[]`. It reads the bundled catalog rather than the current directory.
It reports candidates, not compatibility guarantees or automatic edits.

## Catalog provenance and updates

The bundled 52-entry snapshot comes from
[`python-e18e/module-replacements` at `11adf2086ae70f8143446f4fad46d544040a7128`](https://github.com/python-e18e/module-replacements/blob/11adf2086ae70f8143446f4fad46d544040a7128/replacements.json),
under the same MIT license. The catalog is the source of truth; contribute data
there first. To refresh this repo, choose and review a catalog commit, fetch its
file, update this provenance link and entry count, then run the checks:

```sh
catalog_ref=11adf2086ae70f8143446f4fad46d544040a7128
gh api "repos/python-e18e/module-replacements/contents/replacements.json?ref=$catalog_ref" --jq .content > /tmp/python-e18e-catalog.b64
base64 -d /tmp/python-e18e-catalog.b64 > skills/module-replacements/replacements.json
python checks/check_skills.py
```

Review the diff before publishing. Bump `version` in both plugin JSON files when
shipping updated skills or data so cached plugin installations can receive it.
No automatic migrations or upstream contact are performed by this repository.

## Contributing

Keep skills in `skills/<name>/SKILL.md` with matching `name` and a specific
`description` in YAML frontmatter. Keep helpers offline where practical, preserve
source evidence and migration caveats, and run the checks above before opening
a pull request. Track cross-project opportunities in
[ecosystem-issues](https://github.com/python-e18e/ecosystem-issues).

## License

MIT. Repository structure inspired by e18e/skills; Python instructions and
matcher are maintained independently.
