#!/bin/bash
cd title_page
xelatex strona_tytulowa-jeden-autor.tex
cd ..

echo "...::: Compiled title page :::..."


echo "...::: TODO: Exported diagrams :::..."

pdflatex main.tex
pdflatex main.tex # twice because of the table of contents bug
echo "...::: Compiled thesis :::..."
