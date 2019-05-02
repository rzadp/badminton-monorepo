#!/bin/bash
ROOT_DIR="$(realpath ..)"

docker run -it -v "$(realpath ..)":/root/host badminton_image:latest /bin/bash -c "cd host/badminton && ./train.sh"
echo "Done."
