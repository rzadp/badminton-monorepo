#!/bin/bash
set -e
cd $(dirname $0)

command -v node || { echo "node not found"; exit -1; }

cd ..
for file in ./**/*.mmd; do ../node_modules/.bin/mmdc -i $file -o $(basename "$file" .mmd).png; done
