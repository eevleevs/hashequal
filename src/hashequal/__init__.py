#! /usr/bin/env python3

# a Python module to make quasi interactive math sheets
# https://github.com/eevleevs/hashequal

import datetime
import inspect
import re
import shutil

# load caller script
caller_filename = inspect.getframeinfo(inspect.stack()[-1][0]).filename
if caller_filename == '<stdin>':
    raise ImportError('hashequal cannot be imported in interactive mode')
with open(caller_filename, encoding='utf-8') as file:
    s1 = file.read()

# assign a progressive number to every #=, e.g. "#=/number/"
counter = 0
def replacer(m):
    global counter
    counter += 1
    return f'{m[1]}#=/{counter}/'
s1 = re.sub(r'^([^#]*)#=', replacer, s1, flags=re.M)

# remove line continuations
s2 = s1.replace('\\\n', '')

# substitute "import hashequal" with "pass"
s2 = re.sub(r'^(\s+).*?import hashequal.*$', r'\1pass', s2, flags=re.M)

# prepend "hashequal_data[number] = " to every line with a "#=/number/"
s2 = re.sub(r'(\s*)(.*?)#=\/(\d+)\/(.*)', r'\1hashequal_data[\3] = \2', s2)

# execute s2 retrieving hashequal_data
hashequal_data = {}
exec(s2, {'hashequal_data':hashequal_data, '__name__':'__main__'})

# substitute results in s1
for key,value in hashequal_data.items():
    s1 = re.sub(r'#=\/' + str(key) + r'\/.*?(#.*)?$',
        lambda m: f'#= {value}' + (f'  {m[1]}' if m[1] else ''),
        s1, flags=re.M)

# clear keys that were not evaluated
s1 = re.sub(r'#=\/.*?(#.*)?$', r'#= n/a  \1', s1, flags=re.M)
s1 = re.sub(r'#=  $', r'#= n/a', s1, flags=re.M)

# mark run time
s1 = re.sub(r'(.*?import hashequal).*', r'\1  #/ run '
    + str(datetime.datetime.utcnow()).split('.')[0] + ' UTC', s1)

# overwrite caller script, possibly making a backup
shutil.copyfile(caller_filename, caller_filename + '~')
with open(caller_filename, 'w', encoding='utf-8') as file:
    file.write(s1)

# stop execution
exit()
