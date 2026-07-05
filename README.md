# lizard-standalone

Standalone binary distribution of [**lizard**](https://github.com/terryyin/lizard) — an extensible
Cyclomatic Complexity Analyzer for many programming languages.

This repository wraps `lizard` as a single-file executable so you can run it on machines **without a
Python environment**.

---

## Features

- **Zero dependencies** – one self-contained binary per platform
- **Same CLI as upstream lizard** – drop-in replacement
- **Pre-built releases** for Windows, macOS (Intel & Apple Silicon), and Linux
- **Multiprocessing support** – multithreaded analysis works out of the box

---

## Installation

### Download a pre-built binary

Each release ships a curated set of lizard versions for every platform. The asset name encodes both:
`lizard-<VERSION>-<PLATFORM>`.

To fetch the **latest build of a chosen lizard version**, use the stable `releases/latest/download/...`
URL — it always points at the most recent release containing that version, with no scripting required:

```bash
# Example: latest build of lizard 1.21.7 for Linux
curl -L -o lizard https://github.com/bianjp/lizard-standalone/releases/latest/download/lizard-1.21.7-linux-amd64
chmod +x lizard
./lizard --help
```

Swap in your lizard version and platform suffix:

| Platform                      | Platform suffix            |
|-------------------------------|----------------------------|
| Linux (x64)                   | `linux-amd64`              |
| Windows (x64)                 | `windows-amd64.exe`        |
| macOS (x64 / Intel)           | `darwin-amd64`             |
| macOS (ARM64 / Apple Silicon) | `darwin-arm64`             |

See the [Releases](https://github.com/bianjp/lizard-standalone/releases) page for the list of
available lizard versions.

> **Linux users:** Pre-built Linux binaries require **glibc 2.17+** (e.g. CentOS/RHEL 7+, Ubuntu
> 14.04+, Debian 8+). CI builds use
> [Python Build Standalone](https://github.com/astral-sh/python-build-standalone) so the PyInstaller
> bundle does not inherit the newer glibc requirement of official CPython on recent Ubuntu runners.
> Check with `ldd --version` if you see `GLIBC_2.xx not found` errors.

> **macOS users:** Binaries downloaded from the browser may carry the `com.apple.quarantine`
> extended attribute.
> If a script calling the binary fails silently, run `xattr -cr ./lizard` once.

### Pin to a specific build

The `releases/latest/download/...` URL moves forward as new releases are cut. To pin an **exact**
build, use its date tag (`YYYY-MM-DD`):

```bash
curl -L -o lizard https://github.com/bianjp/lizard-standalone/releases/download/2026-06-18/lizard-1.21.7-linux-amd64
chmod +x lizard
```

> **Note:** once a lizard version is removed from the curated list, its
> `releases/latest/download/lizard-<VERSION>-...` URL stops resolving. Pin a date-tagged release that
> still contains it.

### Build from source

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pyinstaller --onefile --name lizard --collect-submodules lizard_ext main.py
# → dist/lizard
```

---

## Usage

The binary exposes the exact same interface as the upstream `lizard` command.

```bash
# Analyze a single file
./lizard src/main.cpp

# Analyze a directory with 4 worker threads
./lizard -t 4 src/

# Output HTML report
./lizard -H -o report.html src/

# Show only warnings (clang format)
./lizard -w -C 10 src/
```

See `lizard --help` or the [upstream documentation](https://github.com/terryyin/lizard) for the full
option list.

---

## Development

```bash
# Install dependencies
uv sync

# Run lizard from source
uv run python main.py --help

# Build locally
uv run pyinstaller --onefile --name lizard --collect-submodules lizard_ext main.py
```

---

## Release process

Releases are tagged by date (`YYYY-MM-DD`), and each release ships every lizard version listed in
[`lizard-versions.txt`](./lizard-versions.txt) for all supported platforms. The lizard version lives
in the asset filename, not the tag.

```bash
# 1. Edit lizard-versions.txt to add/remove a lizard version (if needed)
# 2. Commit and push
# 3. Create and push a date tag
git tag 2026-06-18
git push origin 2026-06-18
```

GitHub Actions builds every listed version × platform and attaches the artifacts to a release
automatically. Same-day rebuilds use a `-N` suffix (e.g. `2026-06-18-1`).

---

## How it works

- `main.py` is a thin wrapper around `lizard.main()`.
- `multiprocessing.freeze_support()` is called so that `lizard`'s internal `multiprocessing.Pool`
  works correctly inside a PyInstaller bundle.
- PyInstaller is invoked with `--collect-submodules lizard_ext` so dynamically loaded extensions
  (e.g. `lizard_ext.lizardmodified` for `-m`) are included in the bundle.
- On **Linux**, CI installs Python via [uv](https://docs.astral.sh/uv/) from
  [Python Build Standalone](https://github.com/astral-sh/python-build-standalone/releases) rather
  than `actions/setup-python`. PyInstaller embeds the build-time `libpython`, so this keeps the
  minimum glibc at **2.17** instead of the higher version required by official CPython 3.14 on
  recent Ubuntu. Windows and macOS still use `actions/setup-python`.
- GitHub Actions builds the binary on native runners for every supported platform and attaches the
  artifacts to releases automatically.

---

## License

- **This repository** (wrapper code): MIT — see [LICENSE](./LICENSE).
- **Pre-built binaries** bundle [lizard](https://github.com/terryyin/lizard), which is licensed
  under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
