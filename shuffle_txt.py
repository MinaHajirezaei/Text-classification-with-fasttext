


import random
lines = open('fastai_6lbl_compile.txt').readlines()
random.shuffle(lines)

open('fastai_6lbl_compile.txt', 'w').writelines(lines)