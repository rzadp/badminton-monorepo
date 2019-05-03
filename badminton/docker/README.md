## Build

- `docker build ./ -t badminton_image`

## Upload

- `docker tag badminton_image eu.gcr.io/badminton/badminton_image`
- `docker push eu.gcr.io/badminton/badminton_image`

## Run

- `docker run -it -v ~/:/host -p 8888:8888 -p 6006:6006 badminton_image:latest /bin/bash`
- Exposes ports for jupyter notebooks and tesorboard
- Maps current directory to /host on docker
