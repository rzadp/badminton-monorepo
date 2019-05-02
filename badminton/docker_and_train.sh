#!/bin/bash
ROOT_DIR="$(realpath ..)"

docker run -it -v "$(realpath ..)":/root/host eu.gcr.io/badminton/badminton_image /bin/bash -c "cd host/badminton && ./train.sh"
echo "Done."
