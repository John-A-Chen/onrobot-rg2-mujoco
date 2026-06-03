"""MuJoCo loading helpers for examples and smoke tests."""

from __future__ import annotations

from pathlib import Path

import mujoco


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_model(xml_name: str = "scene.xml") -> mujoco.MjModel:
    xml_path = repo_root() / xml_name
    return mujoco.MjModel.from_xml_path(str(xml_path))


def describe_model(model: mujoco.MjModel, label: str = "model") -> str:
    return (
        f"{label}: OK "
        f"nq={model.nq} nv={model.nv} nu={model.nu} "
        f"njnt={model.njnt} ngeom={model.ngeom} neq={model.neq} nkey={model.nkey}"
    )
