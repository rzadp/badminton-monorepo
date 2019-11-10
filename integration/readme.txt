Sieć wytrenowana była na 'dolnych' zdjęciach.

Instrukcja:

1. Wymagania systemowe
- python3.5 (z powodu niekompatybilności nie działa na najnowszym 3.7)
- pip3
- karta graficzna nie jest wymagana (detekcja działa wolniej, ale działa)

2. Instalacja zależności
$ pip3 install -r requirements.txt

3. Detekcja
$ python3.5 detect.py [PATH_TO_IMAGE]... [--OUTPUT=./output]
Na przykład:
$ python3.5 detect.py input/1564906502209808048.jpg input/1564925857424277389.jpg
$ python3.5 detect.py input/1564906502209808048.jpg --OUTPUT=../elsewhere

4. Wynik
W katalogu output, dla każdego obrazu wejściowego jest para obrazów wynikowych:
- mask_xxx.jpg - sama maska kortu na czarnym tle
- visualization_xxx.jpg - przezroczysta maska kortu naniesiona na obrazek wejściowy


Oprócz uruchomienia lokalnie, program przetestowałem na czystych serwerach DigitalOcean aby upewnić się że nie ma jakichś niepisanych zalezności.
Testowałem na Ubuntu 16.04.6 x64 oraz na Fedora 30 x64.
