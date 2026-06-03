# UR3e + RG2 Asset Notes

This asset entry documents the main robot model:

- Robot: Universal Robots UR3e
- Gripper: OnRobot RG2
- Main scene: `../../scene.xml`
- Full robot include: `../../ur3e_rg2.xml`
- Gripper-only include: `../../rg2.xml`

The model uses relative mesh paths, so it can be cloned and loaded from any machine
without editing XML file paths.

Frame rotations in `ur3e_rg2.xml` are matched against the ROS 2 URDF and use MJCF quaternions for multi-axis orientations.
