#!/usr/bin/env python

from functools import reduce
import base64
import csv
import enum
import importlib as imp
import json
import os
import pprint as pp
import re
import shutil
import sys

def analyze(file, provided):
    with open(file) as f:
        lines = f.readlines()
        loc = len(list(filter(lambda line: line != '\n',lines))) - provided
        comp = len(list(filter(lambda line: line.find('if') > -1, lines))) + 1
        return loc, comp

def main(args):
    loc_file = open('loc.csv', 'wt')
    comp_file = open('complexity.csv', 'wt')
    loc_file.write("id,AfablTask1,AfablTask2,scalaTask1,scalaTask2\n")
    comp_file.write("id,AfablTask1,AfablTask2,scalaTask1,scalaTask2\n")
    for dir in os.listdir('submissions'):
        base_path = os.path.join('submissions',dir,'src','main','scala','org','afabl','study')
        a1_loc, a1_comp = analyze(os.path.join(base_path,'AfablTask1.scala'), 20)
        a2_loc, a2_comp = analyze(os.path.join(base_path,'AfablTask2.scala'), 23)
        s1_loc, s1_comp = analyze(os.path.join(base_path,'scalaTask1.scala'), 20)
        s2_loc, s2_comp = analyze(os.path.join(base_path,'scalaTask2.scala'), 20)
        loc_file.write("{},{},{},{},{}\n".format(dir,a1_loc, a2_loc, s1_loc, s2_loc))
        comp_file.write("{},{},{},{},{}\n".format(dir,a1_comp, a2_comp, s1_comp, s2_comp))



if __name__=='__main__':
    main(sys.argv)
