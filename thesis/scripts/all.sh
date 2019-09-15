#!/bin/bash
set -e
cd $(dirname $0)

cd ../title_page
xelatex strona_tytulowa-jeden-autor.tex
cd ../scripts
echo "...::: Compiled title page :::..."

# java -jar $PLANTUML_JAR ./chapters/**/*.plantuml
./mermaid.sh
echo "...::: Exported diagrams :::..."

cd ..
for i in {1..2}; do # twice because of the table of contents bug
  max_in_open=32 pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 main.tex
done

echo "...::: Compiled thesis :::..."
