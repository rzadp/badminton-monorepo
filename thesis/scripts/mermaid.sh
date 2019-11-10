#!/bin/bash
set -e
cd $(dirname $0)
NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

command -v node || { echo "node not found"; exit -1; }

cd ..
find . -name '*.mmd' | while read file; do
  OUTPUT="$(dirname "$file")"/"$(basename "$file" .mmd).png"
  ./node_modules/.bin/mmdc -i $file -o "$OUTPUT" -p ./scripts/puppeteer-config.json
done
