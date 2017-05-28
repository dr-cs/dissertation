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

# class EventType(enum.Enum):
#     USER_IDLE = 0
#     USER_ACTIVE = 1
#     FILE_INACTIVE = 2
#     FILE_ACTIVE = 3

class Event:
    def __init__(self, time, type, file):
        self.time = time
        self.type = type
        self.file = file

    def __str__(self):
        return "Event({}, {}, {})".format(self.time, self.type, self.file)

    def __repr__(self):
        return str(self)

class Task:
    def __init__(self, name):
        self.name = name
        self.time = 0
        self.chunk_start = 0
        self.active = False

    def is_idle(self, event):
        return ((event.type == 'USER_IDLE') or (event.type == 'SUBMIT_OPEN') or
                ((event.type == 'FILE_INACTIVE') and (event.file == self.name)))

    def is_active(self, event):
        return (event.file == self.name) and \
            ((event.type == 'USER_ACTIVE') or (event.type == 'FILE_ACTIVE'))


    def record(self, event):
        if self.is_active(event) and not self.active:
            self.chunk_start = event.time
            self.active = True
        elif self.is_idle(event) and self.active:
           self.time = self.time + (event.time - self.chunk_start)
           self.active = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


def tic2events(tic):
    """Takes a tic in the form {'time': 1484521040, 'actions':
    [{'FILE_ACTIVE': 'AfablTask1.scala'}, {'FILE_INACTIVE': 'scalaTask1.scala'}]}
     and returns a list of Events"""
    # print("Processing {}".format(tic))
    time = tic['time']
    actions = tic['actions']
    if ((type(actions[0]) == str) or ('PROJECT_OPEN' in actions[0].keys())):
        # Only has a non-file-related event
        return []
    # Need func below because d1.update(d2) returns None instead of
    # d1, and Python doesn't have real lambda functions
    def add_dicts(d1, d2): d1.update(d2); return d1
    file_actions = reduce(add_dicts, filter(lambda a: type(a) == dict, actions))
    events = [Event(time, type, file) for type,file in file_actions.items()]
    # print("Turned this tic: {}".format(tic))
    # print("Into these Events: {}\n".format(events))
    return events

def main(args):
    time_file = open('times.csv', 'wt')
    time_file.write("id,AfablTask1,AfablTask2,scalaTask1,scalaTask2\n")
    for dir in os.listdir('submissions'):
        afabl1 = Task('AfablTask1.scala')
        afabl2 = Task('AfablTask2.scala')
        scala1 = Task('scalaTask1.scala')
        scala2 = Task('scalaTask2.scala')
        submission = [s for s in os.listdir(os.path.join('submissions', dir)) if s.endswith("json")][0]
        submission_path = os.path.join('submissions', dir, submission)
        data = json.load(open(submission_path))
        for tic in data['history']['events']:
            for event in tic2events(tic):
                afabl1.record(event)
                afabl2.record(event)
                scala1.record(event)
                scala2.record(event)
        report = "{}: {}, {}: {}, {}: {}, {}: {} ".format(afabl1, afabl1.time,
                                                          afabl2, afabl2.time,
                                                          scala1, scala1.time,
                                                          scala2, scala2.time)
        print("Report: {}".format(dir))
        print(report)
        time_file.write("{},{},{},{},{}\n".format(dir,afabl1.time, afabl2.time, scala1.time, scala2.time))



if __name__=='__main__':
    main(sys.argv)
