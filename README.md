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

Grab the latest release for your platform from
the [Releases](https://github.com/bianjp/lizard-standalone/releases) page.

| Platform                      | Asset                      |
|-------------------------------|----------------------------|
| Linux (x64)                   | `lizard-linux-amd64`       |
| Windows (x64)                 | `lizard-windows-amd64.exe` |
| macOS (x64 / Intel)           | `lizard-darwin-amd64`      |
| macOS (ARM64 / Apple Silicon) | `lizard-darwin-arm64`      |

```bash
# Example: Linux
# Rename the binary to `lizard` (or `lizard.exe` on Windows) for ease of use
mv lizard-linux-amd64 lizard
chmod +x lizard
./lizard --help
```

> **macOS users:** Binaries downloaded from the browser may carry the `com.apple.quarantine`
> extended attribute.
> If a script calling the binary fails silently, run `xattr -cr ./lizard-darwin-*` once.

### Pin to a specific version

Use the release tag to pin an exact version:

```bash
curl -LO https://github.com/bianjp/lizard-standalone/releases/download/v1.21.7-1/lizard-linux-amd64
mv lizard-linux-amd64 lizard
chmod +x lizard
```

### Always fetch the latest build of a given lizard version

```bash
VERSION="1.21.7"
LATEST_TAG=$(curl -s "https://api.github.com/repos/bianjp/lizard-standalone/releases" \
  | jq -r "[.[] | select(.tag_name | startswith(\"v${VERSION}\"))] | first | .tag_name")

curl -LO "https://github.com/bianjp/lizard-standalone/releases/download/${LATEST_TAG}/lizard-linux-amd64"
mv lizard-linux-amd64 lizard
chmod +x lizard
```

### Build from source

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pyinstaller --onefile --name lizard main.py
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
uv run pyinstaller --onefile --name lizard main.py
```

---

## Release process

Version tags follow the pattern `v{LIZARD_VERSION}-{BUILD_NUMBER}`, where the build number starts
from 1.

| Tag         | Meaning                                 |
|-------------|-----------------------------------------|
| `v1.21.7-1` | First build based on lizard 1.21.7      |
| `v1.21.7-2` | Packaging / CI fix; lizard still 1.21.7 |
| `v1.21.8-1` | New upstream lizard version             |

```bash
# 1. Update lizard version in pyproject.toml if needed
# 2. Commit and push
# 3. Create and push a tag
git tag v1.21.7-1
git push origin v1.21.7-1
```

GitHub Actions will build for all platforms and create a release automatically.

---

## How it works

- `main.py` is a thin wrapper around `lizard.main()`.
- `multiprocessing.freeze_support()` is called so that `lizard`'s internal `multiprocessing.Pool`
  works correctly inside a PyInstaller bundle.
- GitHub Actions builds the binary on native runners for every supported platform and attaches the
  artifacts to releases automatically.

---

## License

- **This repository** (wrapper code): MIT — see [LICENSE](./LICENSE).
- **Pre-built binaries** bundle [lizard](https://github.com/terryyin/lizard), which is licensed
  under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
