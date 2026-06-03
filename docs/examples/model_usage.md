# Model Usage

Use the gripper-only MJCF in another robot:

```xml
<include file="path/to/onrobot-rg2-mujoco/rg2.xml"/>
```

Use the full UR3e + RG2 model:

```xml
<include file="path/to/onrobot-rg2-mujoco/ur3e_rg2.xml"/>
```

Use the demo scene with actuators, cube, floor, and home keyframe:

```bash
python3 - <<'PY'
import mujoco

model = mujoco.MjModel.from_xml_path("scene.xml")
print(model.nq, model.nv, model.nu)
PY
```

The full demo scene has seven actuators:

- `ctrl[0:6]`: UR3e arm position targets
- `ctrl[6]`: RG2 gripper target, where `0.0` is open and `0.8` is closed

The included XML files use relative paths. Keep the `external/` submodules initialized when loading the models from a fresh clone.
