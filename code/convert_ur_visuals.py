#!/usr/bin/env python3
"""Convert official UR Collada visual meshes into OBJ files for MuJoCo."""

from __future__ import annotations

from pathlib import Path

import trimesh


ROOT = Path(__file__).resolve().parents[1]
UR_VISUAL_SOURCE = (
    ROOT
    / "external"
    / "Universal_Robots_ROS2_Description"
    / "meshes"
    / "ur3e"
    / "visual"
)
UR_VISUAL_OUTPUT = ROOT / "meshes" / "ur3e" / "visual"
MESH_NAMES = ("base", "shoulder", "upperarm", "forearm", "wrist1", "wrist2", "wrist3")


def _as_mesh(loaded: trimesh.Trimesh | trimesh.Scene) -> trimesh.Trimesh:
    if isinstance(loaded, trimesh.Trimesh):
        return loaded
    if not isinstance(loaded, trimesh.Scene):
        raise TypeError(f"Unsupported mesh type: {type(loaded)!r}")

    meshes = []
    for node_name in loaded.graph.nodes_geometry:
        transform, geometry_name = loaded.graph[node_name]
        mesh = loaded.geometry[geometry_name].copy()
        mesh.apply_transform(transform)
        meshes.append(mesh)

    if not meshes:
        raise ValueError("Scene did not contain any mesh geometry")
    return trimesh.util.concatenate(meshes)


def convert_meshes() -> None:
    UR_VISUAL_OUTPUT.mkdir(parents=True, exist_ok=True)
    for name in MESH_NAMES:
        source = UR_VISUAL_SOURCE / f"{name}.dae"
        output = UR_VISUAL_OUTPUT / f"{name}.obj"
        mesh = _as_mesh(trimesh.load(source, force="scene"))
        mesh.export(output)
        print(f"{source.relative_to(ROOT)} -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    convert_meshes()
