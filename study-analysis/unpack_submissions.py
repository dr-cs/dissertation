#!/usr/bin/env python

import base64
import csv
import importlib as imp
import json
import os
import pprint as pp
import re
import shutil
import sys

def setup_grading_dir(submission_dir, prismid):
    attachments_dir = os.path.join(submission_dir, "Submission attachment(s)")
    if os.path.exists(prismid):
        shutil.rmtree(prismid)
    os.makedirs(prismid)
    for f in os.listdir(attachments_dir):
        shutil.copy(os.path.join(attachments_dir, f), os.path.join(prismid, f))

def main(args):
    for dir in os.listdir('submissions'):
        submission = os.listdir(os.path.join('submissions', dir))[-1]
        submission_path = os.path.join('submissions', dir, submission)
        data = json.load(open(submission_path))
        afabl1 = str(base64.b64decode(data['files'][0]['contents']), 'utf-8')
        afabl2 = str(base64.b64decode(data['files'][1]['contents']), 'utf-8')
        scala1 = str(base64.b64decode(data['files'][2]['contents']), 'utf-8')
        scala2 = str(base64.b64decode(data['files'][3]['contents']), 'utf-8')
        src_dir = os.path.join('submissions', dir, 'src', 'main', 'scala',
                               'org', 'afabl', 'study')
        if not os.path.exists(src_dir): os.makedirs(src_dir)
        afabl1_file = os.path.join(src_dir, 'AfablTask1.scala')
        afabl2_file = os.path.join(src_dir, 'AfablTask2.scala')
        scala1_file = os.path.join(src_dir, 'scalaTask1.scala')
        scala2_file = os.path.join(src_dir, 'scalaTask2.scala')
        with open(afabl1_file, 'wt') as f: f.write(afabl1)
        with open(afabl2_file, 'wt') as f: f.write(afabl2)
        with open(scala1_file, 'wt') as f: f.write(scala1)
        with open(scala2_file, 'wt') as f: f.write(scala2)

    # bulk_download_dir = sys.argv[1]
    # t2_grades_file = "{}/{}".format(bulk_download_dir,"grades.csv")
    # clean_t2_grades_file(t2_grades_file)
    # name2prismid = mk_name_lookup(t2_grades_file)
    # ass = os.getcwd().split('/')[-1]
    # grades_file_name =  ass + ".csv"
    # grader = None
    # try:
    #     grader_module_name = ass + "_grader"
    #     print("Importing {}...".format(grader_module_name), end="")
    #     grader = imp.import_module(grader_module_name)
    #     print("success.")
    # except Exception as e:
    #     print("failed: {}".format(str(e)))
    # print(grader)
    # with open(grades_file_name, 'w') as grades_file:
    #     for rel_path in os.listdir(bulk_download_dir):
    #         name = rel_path.split("(")[0]
    #         submission_dir = os.path.join(bulk_download_dir, rel_path)
    #         if os.path.isdir(submission_dir):
    #             print("Grading {}...".format(name))
    #             setup_grading_dir(submission_dir, name2prismid[name])
    #             grade_report = grader.grade(name2prismid[name]) \
    #                            if grader else -1, "No grader for {}".format(ass)
    #             report_line = "{};{};{};{}".format(name,
    #                                                name2prismid[name],
    #                                                *grade_report)
    #             grades_file.write(report_line + "\n")


if __name__=='__main__':
    main(sys.argv)
