#!/usr/bin/env python3
"""Repo-style entry point for the interactive viewer."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_DEMO = ROOT / "demo.py"


def main() -> None:
    spec = importlib.util.spec_from_file_location("onrobot_rg2_root_demo", ROOT_DEMO)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {ROOT_DEMO}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()


if __name__ == "__main__":
    main()
