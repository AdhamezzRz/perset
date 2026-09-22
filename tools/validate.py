#!/usr/bin/env python3
"""
Validate the Per Set theme without a build step.

Checks:
  1. Every {% schema %} block in sections/ and blocks/ is valid JSON.
  2. Every file in templates/, config/ and locales/ parses as JSON.
  3. Liquid block tags are balanced in every .liquid file.
  4. Every {% render %} / {% include %} target actually exists in snippets/.
  5. Every asset referenced with | asset_url exists in assets/.

Exit code is non-zero if anything fails, so it works in CI.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIRED_TAGS = [
    "if", "for", "form", "paginate", "schema", "stylesheet", "javascript",
    "case", "capture", "unless", "comment", "tablerow", "style", "raw",
]

problems = []


def fail(where, msg):
    problems.append(f"{where}: {msg}")


def check_json_files():
    for pattern in ("templates/**/*.json", "config/*.json", "locales/*.json",
                    "sections/*.json", "blocks/*.json"):
        for path in ROOT.glob(pattern):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(path.relative_to(ROOT), f"invalid JSON — {exc}")


def check_schemas():
    for path in list(ROOT.glob("sections/*.liquid")) + list(ROOT.glob("blocks/*.liquid")):
        src = path.read_text(encoding="utf-8")
        match = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}", src, re.S)
        if not match:
            if path.parent.name == "sections":
                fail(path.relative_to(ROOT), "no {% schema %} block")
            continue
        try:
            json.loads(match.group(1))
        except Exception as exc:
            fail(path.relative_to(ROOT), f"schema is not valid JSON — {exc}")


def check_tag_balance():
    for path in ROOT.rglob("*.liquid"):
        src = path.read_text(encoding="utf-8")
        for tag in PAIRED_TAGS:
            opens = len(re.findall(r"\{%-?\s*" + tag + r"(?:\s|%|-)", src))
            closes = len(re.findall(r"\{%-?\s*end" + tag + r"\s*-?%\}", src))
            if opens != closes:
                fail(path.relative_to(ROOT),
                     f"unbalanced {{% {tag} %}} — {opens} open, {closes} close")


def check_renders():
    snippets = {p.stem for p in ROOT.glob("snippets/*.liquid")}
    for path in ROOT.rglob("*.liquid"):
        src = path.read_text(encoding="utf-8")
        for name in re.findall(r"\{%-?\s*(?:render|include)\s+'([^']+)'", src):
            if name not in snippets:
                fail(path.relative_to(ROOT), f"renders missing snippet '{name}'")


def check_assets():
    have = {p.name for p in ROOT.glob("assets/*")}
    for path in ROOT.rglob("*.liquid"):
        src = path.read_text(encoding="utf-8")
        for name in re.findall(r"'([^']+\.(?:css|js))'\s*\|\s*asset_url", src):
            if name not in have:
                fail(path.relative_to(ROOT), f"references missing asset '{name}'")


def check_blank_defaults():
    """Shopify rejects an empty-string default on a setting. To ship a setting
       as 'unset', omit the default key entirely rather than defaulting it to
       "". This is only caught at upload time otherwise, which is far too late."""
    targets = [ROOT / "config" / "settings_schema.json"]
    targets += list(ROOT.glob("sections/*.liquid")) + list(ROOT.glob("blocks/*.liquid"))

    for path in targets:
        if path.suffix == ".json":
            if not path.exists():
                continue
            try:
                groups = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue  # already reported by check_json_files
            blocks = [g for g in groups if isinstance(g, dict)]
        else:
            src = path.read_text(encoding="utf-8")
            match = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}", src, re.S)
            if not match:
                continue
            try:
                schema = json.loads(match.group(1))
            except Exception:
                continue
            blocks = [schema] + schema.get("blocks", [])

        for group in blocks:
            for setting in group.get("settings", []):
                if setting.get("default") == "":
                    fail(path.relative_to(ROOT),
                         f"setting '{setting.get('id')}' has an empty default — "
                         f"omit the key instead, Shopify rejects it")


def check_piped_filter_args():
    """A piped expression can only be the LAST argument to a Liquid filter.

    Written as `alt: product.title | escape, class: 'x'`, Liquid reads the pipe
    as starting a new filter on the whole tag and then trips over the comma.
    Shopify rejects the file, and when the upload is done by URL it does so
    silently, so this is worth catching locally."""
    arg = re.compile(r"^\s*[a-z_]+:\s+[^,'\"]*\|[^,]*,\s*$")
    for path in ROOT.rglob("*.liquid"):
        src = path.read_text(encoding="utf-8")
        in_output = False
        for i, line in enumerate(src.splitlines(), 1):
            # Only applies inside a multi-line {{ ... }} output tag.
            if "{{" in line and "}}" not in line:
                in_output = True
            elif "}}" in line:
                in_output = False
            if in_output and arg.match(line):
                fail(f"{path.relative_to(ROOT)}:{i}",
                     f"piped filter is not the last argument — {line.strip()}")

        # Single-line form: image_tag: a: x | f, b: y
        for i, line in enumerate(src.splitlines(), 1):
            if re.search(r"\|\s*image_tag:.*\|[^|,]*,\s*[a-z_]+:", line):
                fail(f"{path.relative_to(ROOT)}:{i}",
                     "piped filter is not the last argument to image_tag")


def main():
    check_json_files()
    check_schemas()
    check_blank_defaults()
    check_piped_filter_args()
    check_tag_balance()
    check_renders()
    check_assets()

    counts = {
        "sections": len(list(ROOT.glob("sections/*.liquid"))),
        "snippets": len(list(ROOT.glob("snippets/*.liquid"))),
        "templates": len(list(ROOT.rglob("templates/**/*"))),
        "assets": len(list(ROOT.glob("assets/*"))),
    }
    summary = "  ".join(f"{k}={v}" for k, v in counts.items())

    if problems:
        print(f"FAILED — {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        print(f"\n{summary}")
        return 1

    print(f"OK — theme validates.\n{summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
