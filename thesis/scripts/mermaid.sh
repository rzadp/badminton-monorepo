#!/bin/zsh
set -e
cd $(dirname $0)

cd ..
for file in ./**/*.mmd; do ../node_modules/.bin/mmdc -i $file -o $(basename "$file" .mmd).png; done
