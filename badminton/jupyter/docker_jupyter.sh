#!/bin/bash
docker run -p 8888:8888 -it -v "$(realpath ../..)":/root/host eu.gcr.io/badminton/badminton_image /bin/bash -c "cd host/badminton/jupyter && ./jupyter.sh"
