# Assets

This folder documents the source assets used by the MJCF files.

The canonical standalone MJCF files remain at the repository root:

- `../rg2.xml`
- `../ur3e_rg2.xml`
- `../scene.xml`

Mesh assets are stored in:

- `../external/Universal_Robots_ROS2_Description/meshes/ur3e/collision/`
- `../external/OnRobot_ROS2_Description/meshes/rg2/collision/`
- `../external/OnRobot_ROS2_Description/meshes/rg2/visual/`
- `../meshes/ur3e/visual/` for MuJoCo-loadable OBJ files converted from official UR `.dae` visual meshes

The local `meshes/` directory intentionally only contains generated UR3e visual OBJs. Collision meshes and RG2 meshes are loaded from submodules to avoid duplicate local copies.
