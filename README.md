# Example control for the Pollen Robotics "AmazingHand" (a.k.a. AH!)

## How to use:
- Install Rust: https://www.rust-lang.org/tools/install
- Install uv: https://docs.astral.sh/uv/getting-started/installation/
- Install dora-rs: https://dora-rs.ai/docs/guides/Installation/installing
  - start the daemon: `dora up`

- Clone this repository and in a console from the directory run:
- `uv venv --python 3.12`
- To run the webcam hand tracking demo in simulation only:
  - `dora build dataflow_tracking_simu.yml --uv` (needs to be done only once)
  - `dora run dataflow_tracking_simu.yml --uv`
- To run the webcam hand tracking demo with real hardware:
  - `dora build dataflow_tracking_real.yml --uv` (needs to be done only once)
  - `dora run dataflow_tracking_real.yml --uv`
- To run a simple example to control the finger angles in simulation:
  - `dora build dataflow_angle_simu.yml --uv` (needs to be done only once)
  - `dora run dataflow_angle_simu.yml --uv`