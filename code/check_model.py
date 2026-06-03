#!/usr/bin/env python3
"""Load the MJCF files and print a compact MuJoCo model summary."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.mujoco_model import describe_model, load_model


def main() -> None:
    for xml_name in ("rg2.xml", "ur3e_rg2.xml", "scene.xml"):
        model = load_model(xml_name)
        print(describe_model(model, xml_name))


if __name__ == "__main__":
    main()
