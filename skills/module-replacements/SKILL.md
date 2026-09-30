---
name: module-replacements
description: Find Python dependencies with standard-library or maintained alternatives using the python-e18e catalog, assess compatibility, and apply requested migrations. Use for Python dependency cleanup, replacing backports, reducing dependencies, or modernizing Python packages and tooling.
---

# Python module replacements

Use the bundled `replacements.json` to find candidates. The catalog is a
researched snapshot, not a guarantee of API parity or improved performance.
The matcher needs only Python 3.11+ and works offline.

## Find candidates

Read the project's supported Python versions, dependency declarations, and
contribution instructions before proposing changes. Inspect `pyproject.toml`
(including optional dependencies, dependency groups, and tool-specific tables),
requirements and constraints files, `setup.cfg`, and relevant CI configuration.
Inspect `setup.py` as text; do not execute project code to discover dependencies.
In a workspace, check each package.

Collect **distribution names**, without extras, specifiers, or environment
markers, and pass them explicitly to the matcher. Keep the original declarations
for compatibility review; never infer a distribution solely from an import name
(`PIL` is Pillow, for example). Trace source imports and call sites to verify
actual use. Distinguish standard-library imports from installed backports.

```sh
python "<skill-dir>/match.py" tomli appdirs backports.zoneinfo
```

`<skill-dir>` is the directory containing this file. The matcher normalizes
PyPI names, removes duplicate matches, and returns a JSON array of the original
catalog entries. An empty array means no known match; it does not certify the
dependency tree. There is no automatic project scan or requirements parser.

Each entry contains `name`, `alternative`, `minimum_python`, `kind`,
`compatibility`, `guidance`, `source`, and `references`. Read the full guidance:

- `drop-in`: dependency declarations can change within the documented scope.
- `import-only`: imports also change within the documented API scope.
- `conditional`: audit every used API and behavior before proposing a swap.
- `code-change`: application, configuration, or workflow changes are required.

`alternative` can list choices separated by `/`; it is not an install command.
`minimum_python` is a feature or researched-release floor, not proof that all
used APIs exist on that version. Check markers and older supported runtimes.
For each viable candidate, report real call sites, the proposed alternative,
compatibility caveats, required checks, and primary evidence links. Maintained
packages may still be appropriate; propose a change only when it fits the project.

## Select and apply

For an audit request, present candidates and ask which migrations to apply.
If the user already requested specific migrations, proceed within that scope.
When alternatives imply different behavior, resolve the choice before editing.

Consult the entry's primary sources for API differences and current release
requirements. Adapt call sites and configuration; do not blindly rename imports.
Keep backports behind markers where older runtimes still need them. Remove a
dependency only after inventorying all uses, including extras and build tooling.
Preserve supported configuration and use the project's existing package manager
to update lockfiles; do not edit generated locks by hand.

Use the [python-e18e codemods](https://github.com/python-e18e/codemods) when their
documented recipe scope fits. Preview the diff with an explicit target Python
floor; broader migrations still need API review. The optional
[MCP server](https://github.com/python-e18e/mcp) exposes the same previews.
Neither tool is required to use this skill.

Run the relevant project tests, lint/type checks, and minimum-runtime checks.
For platform-sensitive changes, check each supported OS; for packaging or
configuration changes, compare built artifacts and diagnostics. Measure any
claimed performance benefit. Report the changes, checks, and remaining caveats.
