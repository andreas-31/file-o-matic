#!/usr/bin/python3
from __future__ import print_function
import os
import re

def hello():
    print('Hello!')
    if os.path.isdir('Downloads'):
        print('Is a directory!')

class Files():
    interesting_stuff = {
        'evtx': '\.evtx',
        'evt': '\.evt',
        'reg_folder': os.path.join('system32', 'config', ''),
        #'reg_folder': 'windows/system32/config',
        'reg_ntuser': 'ntuser\.dat',
        'reg_usrclass': 'usrclass\.dat',
        'setupapi': 'setupapi\.log'
    }
    interesting_files = []

    def __init__(self, directory='.'):
        self.directory = directory
        self.files = []
        self.dirs = []
        self.read_dir(directory)

    def read_dir(self, new_folder):
        #print('read_dir:', folder)
        folder = os.path.abspath(new_folder)
        self.dirs.append(folder)
        onlyfiles = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        self.add_files(onlyfiles)

        for my_file in onlyfiles:
            for key in self.interesting_stuff:
                value = self.interesting_stuff[key]
                if my_file in self.interesting_files:
                    continue
                if re.search(value, my_file, re.IGNORECASE):
                    self.interesting_files.append(my_file)
        
        onlydirs = [os.path.join(folder, d) for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
        for my_dir in onlydirs:
            self.read_dir(my_dir)

    def add_files(self, new_files):
        self.files.extend(new_files)

    def __str__(self):
        return '\n'.join(self.files)

    def str_ifiles(self):
        return '\n'.join(self.interesting_files)

    def count_files(self):
        return len(self.files)

    def count_dirs(self):
        return len(self.dirs)


def main():
    mypath = '/mnt/OS'
    #mypath = '.'
    myFiles = Files(mypath)
    #print(myFiles)
    print(myFiles.str_ifiles())
    print("Count files: {}".format(myFiles.count_files()))
    print("Count dirs: {}".format(myFiles.count_dirs()))
    #onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    #print(onlyfiles)

    #onlydirs = [d for d in os.listdir(mypath) if os.path.isdir(os.path.join(mypath, d))]
    #print(onlydirs)

if __name__ == '__main__':
    main()
