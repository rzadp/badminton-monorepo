#!/bin/bash
set -e
cd $(dirname $0)
NVM_DIR="$HOME/.nvm"

command -v node || \
{ [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" "$NVM_OPTION" } || \
{ echo "node not found"; exit -1; }

cd ..
find . -name '*.mmd' | while read file; do
  ./node_modules/.bin/mmdc -i $file -o $(basename "$file" .mmd).png -p ./scripts/puppeteer-config.json
done
