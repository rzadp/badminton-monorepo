#!/bin/bash
docker run -it -v "$(realpath ../..)":/root/host eu.gcr.io/badminton/badminton_image /bin/bash -c "cd host/badminton/detection && python3 ./detect.py"
