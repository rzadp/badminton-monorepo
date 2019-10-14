#!/bin/bash
cd $(dirname $0)
set -e
ROOT_DIR="$(realpath ../..)"

docker build -t badminton_image .
docker run -it -v "$ROOT_DIR":/mono badminton_image /bin/bash -c "cd /mono/badminton/detection && ./detect.sh weights.h5 input.jpg output.png"

echo "Done."
