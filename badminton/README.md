# badminton

This is built on top of Mask_RCNN submodule.

## Requirements

**Docker** is required in order to run training and detection. All other requirements are satisfied in the docker image.

## Training

(...)

## Detection

- `cd ./detection`
- `./docker_detect.sh`

## Docker

The docker image used in this project is specified in `./docker/Dockerfile`.

## Jupyter notebooks

### Run

- `cd ./jupyter`
- `./docker_jupyter.sh`
- Navigate to http://localhost:8888

### Notebooks

| Subdirectory | Description |
| --- | --- |
| inspect_badminton_data | Notebook for inspecting dataset. |
| run_model | Notebook for visualizing detection. |
