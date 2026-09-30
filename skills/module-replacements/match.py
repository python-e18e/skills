"""Match explicit distribution names against the bundled catalog, offline."""

import argparse
import json
import re
from pathlib import Path


def distribution_name(value):
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?", value):
        raise argparse.ArgumentTypeError(
            f"{value!r}: pass a distribution name without extras, versions, or markers"
        )
    return re.sub(r"[-_.]+", "-", value).lower()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", type=distribution_name)
    args = parser.parse_args()
    catalog = json.loads(
        Path(__file__).with_name("replacements.json").read_text(encoding="utf-8")
    )
    by_name = {distribution_name(entry["name"]): entry for entry in catalog}
    matches = [by_name[name] for name in dict.fromkeys(args.names) if name in by_name]
    print(json.dumps(matches, indent=2))


if __name__ == "__main__":
    main()
