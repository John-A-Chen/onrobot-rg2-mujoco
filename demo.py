#!/usr/bin/env python3
"""Interactive MuJoCo viewer for the UR3e + OnRobot RG2 scene."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import mujoco
import mujoco.viewer

try:
    import glfw
except ImportError:  # MuJoCo viewer normally installs this dependency.
    glfw = None


ARM_JOINTS = [
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
]
GRIPPER_JOINT = "left_driver_joint"
ARM_STEP = 0.05
GRIPPER_OPEN = 0.0
GRIPPER_CLOSED = 0.8
DEFAULT_CUBE_POS = (0.0, -0.35, 0.02)
CUBE_JOINT = "red_cube_freejoint"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interactive MuJoCo viewer for UR3e + OnRobot RG2.")
    parser.add_argument(
        "--cube",
        type=float,
        nargs=3,
        metavar=("X", "Y", "Z"),
        help="Initial red cube position in metres, for example: --cube 0 -0.35 0.02",
    )
    parser.add_argument("--cube-x", type=float, default=None, help="Initial red cube X position in metres.")
    parser.add_argument("--cube-y", type=float, default=None, help="Initial red cube Y position in metres.")
    parser.add_argument("--cube-z", type=float, default=None, help="Initial red cube Z position in metres.")
    return parser.parse_args()


def cube_position_from_args(args: argparse.Namespace) -> tuple[float, float, float]:
    cube_pos = list(args.cube if args.cube is not None else DEFAULT_CUBE_POS)
    for index, value in enumerate((args.cube_x, args.cube_y, args.cube_z)):
        if value is not None:
            cube_pos[index] = value
    return tuple(cube_pos)


def _key_name(key: int) -> str:
    if key == 32:
        return "SPACE"
    try:
        return chr(key)
    except ValueError:
        return str(key)


def _shift_down() -> bool:
    if glfw is None:
        return False
    window = glfw.get_current_context()
    if window is None:
        return False
    return (
        glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
        or glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    )


def main() -> None:
    args = parse_args()
    cube_pos = cube_position_from_args(args)

    xml_path = Path(__file__).with_name("scene.xml")
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    home_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, "home")
    if home_id < 0:
        raise RuntimeError("Missing keyframe named 'home'")
    cube_joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, CUBE_JOINT)
    if cube_joint_id < 0:
        raise RuntimeError(f"Missing joint named {CUBE_JOINT!r}")
    cube_qpos_addr = model.jnt_qposadr[cube_joint_id]

    running = True
    gripper_closed = False

    def apply_cube_position() -> None:
        data.qpos[cube_qpos_addr : cube_qpos_addr + 3] = cube_pos
        data.qpos[cube_qpos_addr + 3 : cube_qpos_addr + 7] = (1.0, 0.0, 0.0, 0.0)

    def reset_home() -> None:
        nonlocal gripper_closed
        data.qpos[:] = model.key_qpos[home_id]
        data.qvel[:] = 0.0
        data.ctrl[:] = model.key_ctrl[home_id]
        apply_cube_position()
        gripper_closed = False
        mujoco.mj_forward(model, data)

    def print_state(key: int) -> None:
        angles = ", ".join(f"{name[:-6]}={data.ctrl[i]: .3f}" for i, name in enumerate(ARM_JOINTS))
        grip = "closed" if gripper_closed else "open"
        print(f"{_key_name(key):>5} | {angles}, gripper={grip} ({data.ctrl[6]:.3f})", flush=True)

    def key_callback(key: int) -> None:
        nonlocal running, gripper_closed

        shift = _shift_down()
        if glfw is not None and key == glfw.KEY_ESCAPE:
            running = False
            return
        if key == ord("Q") and shift:
            running = False
            return

        if key == 32:
            gripper_closed = not gripper_closed
            data.ctrl[6] = GRIPPER_CLOSED if gripper_closed else GRIPPER_OPEN
            print_state(key)
            return

        if key == ord("R") and shift:
            reset_home()
            print_state(key)
            return

        positive_by_number = {
            ord("1"): 0,
            ord("2"): 1,
            ord("3"): 2,
            ord("4"): 3,
            ord("5"): 4,
            ord("6"): 5,
        }
        negative_by_letter = {
            ord("Q"): 0,
            ord("W"): 1,
            ord("E"): 2,
            ord("R"): 3,
            ord("T"): 4,
            ord("Y"): 5,
        }

        if key in positive_by_number:
            data.ctrl[positive_by_number[key]] += ARM_STEP
            print_state(key)
            return

        if key in negative_by_letter and not shift:
            data.ctrl[negative_by_letter[key]] -= ARM_STEP
            print_state(key)
            return

        if key in negative_by_letter and shift:
            data.ctrl[negative_by_letter[key]] += ARM_STEP
            print_state(key)

    reset_home()
    print(f"cube=({cube_pos[0]:.3f}, {cube_pos[1]:.3f}, {cube_pos[2]:.3f})", flush=True)
    with mujoco.viewer.launch_passive(model, data, key_callback=key_callback) as viewer:
        viewer.opt.geomgroup[3] = 0
        while viewer.is_running() and running:
            step_start = time.time()
            mujoco.mj_step(model, data)
            viewer.sync()
            elapsed = time.time() - step_start
            if elapsed < model.opt.timestep:
                time.sleep(model.opt.timestep - elapsed)


if __name__ == "__main__":
    main()
