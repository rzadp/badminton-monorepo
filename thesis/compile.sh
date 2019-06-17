#!/bin/zsh
set -e

cd title_page
xelatex strona_tytulowa-jeden-autor.tex
cd ..

echo "...::: Compiled title page :::..."

java -jar $PLANTUML_JAR ./chapters/**/*.plantuml

echo "...::: Exported diagrams :::..."

max_in_open=32 pdflatex main.tex
max_in_open=32 pdflatex main.tex # twice because of the table of contents bug
echo "...::: Compiled thesis :::..."
