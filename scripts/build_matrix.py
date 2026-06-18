#!/usr/bin/env python3
"""Compute the GitHub Actions build matrix from lizard-versions.txt.

Reads the curated lizard version list, computes the cartesian product of
versions x platforms, and emits the matrix plus the version list as GitHub
Actions outputs when GITHUB_OUTPUT is set. Also prints a JSON payload to
stdout for local inspection and CI logs.

Override the versions file with the VERSIONS_FILE environment variable
(default: lizard-versions.txt in the repository root).
"""

import json
import os
import sys
from pathlib import Path

# Supported build platforms: runner OS, asset target suffix, file extension.
PLATFORMS: list[dict[str, str]] = [
    {"os": "ubuntu-latest", "target": "linux-amd64", "ext": ""},
    {"os": "windows-latest", "target": "windows-amd64", "ext": ".exe"},
    {"os": "macos-15-intel", "target": "darwin-amd64", "ext": ""},
    {"os": "macos-latest", "target": "darwin-arm64", "ext": ""},
]

DEFAULT_VERSIONS_FILE = Path(__file__).resolve().parent.parent / "lizard-versions.txt"


def read_versions(path: Path) -> list[str]:
    """Return the lizard versions listed in ``path``.

    Blank lines and comments (``#`` to end of line) are ignored; surrounding
    whitespace is trimmed. Order is preserved.
    """
    versions: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            versions.append(line)
    return versions


def build_matrix(versions: list[str]) -> list[dict[str, str]]:
    """Cartesian product of ``versions`` x :data:`PLATFORMS`.

    Each entry is ``{**platform, "lizard_version": version}``.
    """
    matrix: list[dict[str, str]] = []
    for version in versions:
        for platform in PLATFORMS:
            entry = {"lizard_version": version}
            entry.update(platform)
            matrix.append(entry)
    return matrix


def render_outputs(versions: list[str], github_output: str | None) -> dict[str, object]:
    """Build the output payload and append it to ``GITHUB_OUTPUT`` when given.

    Writes single-line ``matrix=<json>`` (an ``{"include": [...]}`` object, the
    shape GitHub Actions expects for a dynamic matrix) and ``versions=<json>``
    lines. Returns the payload ``{"matrix": [...], "versions": [...]}`` for
    printing.
    """
    matrix = build_matrix(versions)
    payload: dict[str, object] = {"matrix": matrix, "versions": versions}
    if github_output:
        matrix_json = json.dumps({"include": matrix})
        versions_json = json.dumps(versions)
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={matrix_json}\n")
            fh.write(f"versions={versions_json}\n")
    return payload


def main() -> int:
    versions_file = Path(os.environ.get("VERSIONS_FILE") or DEFAULT_VERSIONS_FILE)
    try:
        versions = read_versions(versions_file)
    except OSError as exc:
        print(f"error: cannot read versions file {versions_file}: {exc}", file=sys.stderr)
        return 1
    if not versions:
        print(f"error: no lizard versions found in {versions_file}", file=sys.stderr)
        return 1
    payload = render_outputs(versions, os.environ.get("GITHUB_OUTPUT"))
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
