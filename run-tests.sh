rm tests/output-*


python maxempty/rect.py -i tests/input-figure-1.jpg -o tests/output-figure-1.jpg -f 255,0,0 -e 255,255,255
# (9240, [(1, 40, 55, 207)])

python maxempty/rect.py --input tests/input-figure-2.jpg --output tests/output-figure-2.jpg --fill 0,255,0 --empty 255,255,255
# (22200, [(23, 208, 207, 327)])

python maxempty/rect.py -i tests/input-figure-3.jpg -o tests/output-figure-3.jpg -f 0,0,255 -e 255,255,255
# (4032, [(0, 136, 63, 198)])

python maxempty/rect.py --input tests/input-figure-4.jpg --output tests/output-figure-4.jpg --fill 255,255,0 --busy 0,0,0
# (11236, [(35, 113, 140, 218)])

python maxempty/rect.py -i tests/input-figure-5.png -o tests/output-figure-5.png -f 255,0,255 -e 255,255,255
# (81081, [(50, 53, 478, 241)])

# python maxempty/rect.py --input tests/input-multiple-squares.png --output tests/output-multiple-squares.png --fill 0,255,255 --empty 255,255,255
