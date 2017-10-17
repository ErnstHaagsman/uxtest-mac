#!/usr/local/bin/python3
import glob
import subprocess
from pathlib import Path
import os
import re

import shutil

RECORDINGS_FOLDER = str(Path(Path.cwd(), 'recordings'))
CAMTASIA_FOLDER = os.path.expanduser('~/Movies/Camtasia 2/')
IDEA_LOGS = os.path.expanduser('~/Library/Logs/PyCharm2017.3/')

# First, stop Camtasia
subprocess.run(["osascript", "stop_recording.scpt"])

# Now, we need to move the recording files
# First, get the user's name
with open('name.txt', 'r') as f:
    name = f.read().strip()


# Create the recordings directory if it doesn't exist
if not Path(RECORDINGS_FOLDER).is_dir():
    os.mkdir(RECORDINGS_FOLDER)

# Get the sequence number for the next recording
# Recordings folders should be named '01 - <Name>', '02 - <Name>', etc.

# This gets all subdirectories of RECORDINGS_FOLDER
# See https://stackoverflow.com/questions/141291/how-to-list-only-top-level-directories-in-python
directories = next(os.walk(RECORDINGS_FOLDER))[1]

next_number = -1
if not directories:
    next_number = 0
else:
    for directory in directories:
        number_path = re.search('^(\d{2})', directory)
        if number_path is None:
            continue

        number = int(number_path.group(1))
        if number > next_number:
            next_number = number

# The next number is one higher than the highest we already have
next_number += 1

# Now we have the name and the number, let's create the folder
folder_name = '{:02d} - {}'.format(next_number, name)

print('Moving recordings into: {}'.format(folder_name))

folder = str(Path(RECORDINGS_FOLDER, folder_name))
os.mkdir(folder)

# Let's copy all found recordings there
for trec_file in glob.iglob(CAMTASIA_FOLDER + '/**/*.trec', recursive=True):
    shutil.move(trec_file, folder)

print('Moving IDEA logs')

# Copy idea logs
shutil.move(IDEA_LOGS, folder)

print('Running reset playbook')

# Reset with Ansible
subprocess.run(["ansible-playbook", "reset.yml"])