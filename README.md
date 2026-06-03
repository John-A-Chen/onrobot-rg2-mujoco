# OnRobot RG2 Gripper - MuJoCo MJCF

Standalone MuJoCo models for an OnRobot RG2 gripper mounted on a Universal Robots UR3e arm.

The goal of this repository is to keep a clean MJCF package that can be opened directly in MuJoCo, while still tracing mesh and frame data back to the ROS 2 description packages it came from.

## What Is Included

- `rg2.xml`: gripper-only MJCF for including the RG2 in another robot.
- `ur3e_rg2.xml`: UR3e kinematic chain with the RG2 mounted at `tool0`, no actuators.
- `scene.xml`: demo world with floor, light, red cube, arm/gripper actuators, and a home keyframe.
- `demo.py`: keyboard-controlled MuJoCo passive viewer.
- `code/check_model.py`: loads all MJCF files and prints a compact model summary.
- `code/convert_ur_visuals.py`: regenerates MuJoCo-loadable UR3e visual OBJs from official UR Collada meshes.

## How It Came Together

The arm and gripper geometry started from ROS 2 description packages:

- Universal Robots' ROS 2 description provides UR3e kinematics, collision meshes, and visual `.dae` meshes.
- Tony Le's OnRobot ROS 2 description provides the RG2 Xacro, collision meshes, and visual meshes.
- The RG2 linkage was written as a MuJoCo 4-bar parallel-jaw mechanism with equality constraints.

MuJoCo cannot load the official UR3e Collada `.dae` visual files in this environment, so those visuals are converted once into OBJ files under `meshes/ur3e/visual/`. Collision meshes are not duplicated locally; they load from the submodules.

The UR3e frame rotations were matched against the ROS 2 URDF/MuJoCo-generated model. Multi-axis rotations use `quat` in MJCF because using equivalent-looking `euler` values produced wrong tool-frame orientation in MuJoCo.

## Layout

```text
.
├── README.md
├── LICENSE
├── rg2.xml
├── ur3e_rg2.xml
├── scene.xml
├── demo.py
├── asset/
│   ├── README.md
│   └── ur3e_rg2/README.md
├── code/
│   ├── check_model.py
│   ├── convert_ur_visuals.py
│   └── demo.py
├── docs/
│   └── examples/
│       ├── model_usage.md
│       └── quick_start.md
├── external/
│   ├── OnRobot_ROS2_Description/              # submodule
│   └── Universal_Robots_ROS2_Description/     # submodule
├── meshes/
│   └── ur3e/
│       └── visual/                            # generated OBJ visuals for MuJoCo
└── model/
    ├── __init__.py
    └── mujoco_model.py
```

There are no local duplicate RG2 meshes or UR3e collision meshes. Those are loaded from `external/`.

## Install

Clone with submodules:

```bash
git clone --recursive git@github.com:John-A-Chen/onrobot-rg2-mujoco.git
cd onrobot-rg2-mujoco
```

If you already cloned it:

```bash
git submodule update --init --recursive
```

Install Python dependencies:

```bash
python3 -m pip install mujoco
```

Only needed if regenerating UR3e visual OBJ meshes:

```bash
python3 -m pip install trimesh pycollada
python3 code/convert_ur_visuals.py
```

## Run

Open the interactive viewer:

```bash
python3 demo.py
```

Spawn the red cube at a custom XYZ position, in metres:

```bash
python3 demo.py --cube 0.05 -0.30 0.02
```

You can also override individual coordinates:

```bash
python3 demo.py --cube-x 0.05 --cube-y -0.30 --cube-z 0.02
```

Alternative repo-style entry point:

```bash
python3 code/demo.py
```

The viewer hides collision geom group `3` by default so the visual model is not covered by rough collision meshes.

## Keyboard Controls

| Key | Action |
| --- | --- |
| Space | Toggle gripper open/close |
| Shift+R | Reset to home pose |
| Escape | Quit |
| Shift+Q | Quit |
| 1 / q | shoulder_pan positive / negative |
| 2 / w | shoulder_lift positive / negative |
| 3 / e | elbow positive / negative |
| 4 / r | wrist_1 positive / negative |
| 5 / t | wrist_2 positive / negative |
| 6 / y | wrist_3 positive / negative |

Joint jog step is `0.05` rad. Gripper control is `ctrl[6]`, where `0.0` is open and `0.8` is closed.

`Shift+R` resets the robot and returns the cube to the command-line spawn position.

## Validate

Check all XML files without opening a GUI:

```bash
python3 code/check_model.py
```

Expected output shape:

```text
rg2.xml: OK ...
ur3e_rg2.xml: OK ...
scene.xml: OK ...
```

## Use In Another MJCF

Gripper only:

```xml
<include file="path/to/onrobot-rg2-mujoco/rg2.xml"/>
```

Full UR3e + RG2 model:

```xml
<include file="path/to/onrobot-rg2-mujoco/ur3e_rg2.xml"/>
```

Add your own actuators in the scene, or copy the actuator block from `scene.xml`.

## Mesh Paths

All mesh paths are relative to the repository:

- UR3e collisions: `external/Universal_Robots_ROS2_Description/meshes/ur3e/collision/`
- UR3e visuals: `meshes/ur3e/visual/*.obj`
- RG2 collisions and visuals: `external/OnRobot_ROS2_Description/meshes/rg2/`

## Credits / License

This package is MIT licensed.

UR3e assets are sourced from Universal Robots' ROS 2 description package. RG2 assets are sourced from Tony Le's OnRobot ROS 2 description package, which credits the Osaka University Harada Laboratory OnRobot model.
