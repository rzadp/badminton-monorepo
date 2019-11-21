#!/bin/bash
set -e
cd $(dirname $0)

cd ../title_page
xelatex -interaction=batchmode -halt-on-error strona_tytulowa-jeden-autor.tex
cd ../scripts
echo "...::: Compiled title page :::..."

# java -jar $PLANTUML_JAR ./chapters/**/*.plantuml
./mermaid.sh
echo "...::: Exported diagrams :::..."

cd ..
# twice because of the table of contents bug
max_in_open=32 pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 main.tex
bibtex main.aux
max_in_open=32 pdflatex -interaction=batchmode -halt-on-error -synctex=1 main.tex
max_in_open=32 pdflatex -interaction=batchmode -halt-on-error -synctex=1 main.tex

echo "...::: Compiled thesis :::..."
