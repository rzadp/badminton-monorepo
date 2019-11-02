#!/bin/bash
cd $(dirname $0)
set -e
ROOT_DIR="$(realpath ../..)"

docker build -t badminton_image .
docker run -e CI -it -v "$ROOT_DIR":/mono badminton_image /bin/bash -c "cd /mono/badminton/training && ./test_and_validate.sh"

echo "Done."
