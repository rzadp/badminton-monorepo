#!/bin/bash
set -e
ROOT_DIR="$(realpath ../..)"

docker build -t badminton_image .
docker run -it -v "$ROOT_DIR":/mono badminton_image /bin/bash -c "cd /mono/badminton/detection && ./detect.sh"

echo "Done."
