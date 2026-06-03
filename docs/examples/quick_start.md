# Quick Start

Run the interactive MuJoCo viewer from the repository root:

```bash
cd /home/john/git/onrobot-rg2-mujoco
git submodule update --init --recursive
python3 -m pip install mujoco
python3 demo.py
```

If the submodules are missing after cloning, run:

```bash
git submodule update --init --recursive
```

The repo-style wrapper also works:

```bash
python3 code/demo.py
```

Spawn the cube somewhere else:

```bash
python3 demo.py --cube 0.05 -0.30 0.02
python3 demo.py --cube-x 0.05 --cube-y -0.30 --cube-z 0.02
```

Controls:

| Key | Action |
| --- | --- |
| Space | Toggle gripper open/close |
| 1 / q | shoulder_pan positive / negative |
| 2 / w | shoulder_lift positive / negative |
| 3 / e | elbow positive / negative |
| 4 / r | wrist_1 positive / negative |
| 5 / t | wrist_2 positive / negative |
| 6 / y | wrist_3 positive / negative |
| Shift+R | Reset home |
| Escape | Quit |
| Shift+Q | Quit |
