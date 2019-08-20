#!/bin/zsh
set -e
cd $(dirname $0)

export NVM_DIR="/Users/przemek/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
nvm use default

cd ..
for file in ./**/*.mmd; do ../node_modules/.bin/mmdc -i $file -o $(basename "$file" .mmd).png; done
