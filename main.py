#!/usr/bin/env python3
"""Entry point for the standalone lizard binary.

This thin wrapper invokes the upstream ``lizard`` CLI while ensuring
multiprocessing compatibility with frozen executables built by
PyInstaller.
"""

import multiprocessing
import sys

from lizard import main


def run() -> int:
    """Execute the lizard CLI and return its exit code."""
    try:
        return main()
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # pragma: no cover
        print(f"Fatal error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Required for multiprocessing.Pool to work inside a PyInstaller bundle.
    multiprocessing.freeze_support()
    sys.exit(run())
