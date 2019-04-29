#!/usr/bin/env python

# a Python module to make quasi interactive math sheets
# https://github.com/eevleevs/hashequal

# congifuration
align_results = False  # if True aligns all results to the rightmost #=

# import
import datetime
import inspect
import json
import os
import re

# init variables
f = inspect.getframeinfo(inspect.stack()[-1][0]).filename  # caller script name
if f == '<stdin>':
    raise ImportError('hashequal cannot be imported in interactive mode')
c = open(f).read().split('\n')  # caller script content lines
p = 0  # alignment counter
s = ''  # aux string
t = 'hashequal_temp'  # temporary file name
e = r'(\s*([\w\d]+)\s*?=?.*?)#=(.*)'  # search pattern

# rewrite caller script to save results of operations marked with #= and save to temporary file
ic = 1
for i in c:
    if 'import hashequal' in i:  # prevent another call of import hashequal
        s += i.replace('import hashequal', 'import chardet; import json; hashequal_data = []') + '\n'  # import other modules and init data container
    else:
        m = re.match(e, i)  # match #= lines
        if m:
            s += m.group(1) + '; hashequal_data.append(\'' + str(ic) + ':\' + str(' + m.group(2) + ').decode(chardet.detect(str(' + m.group(2) + '))[\'encoding\']))\n'  # insert code for saving to temporary variable
            if (len(m.group(1)) > p):
                p = len(m.group(1))  # adjust alignment counter
        else:
            s += i + '\n'
    ic += 1
s += 'open(\'' + t + '\', \'w\').write(json.dumps(hashequal_data))'  # insert code for writing results
open(t, 'w').write(s)  # write modified script

# run modified script, overwrites self with results
if not os.system('python ' + t):

    # load results and rewrite original script to include them as comments
    d = {}
    for i in json.loads(open(t).read()):
        i = i.split(':', 1)
        try:
            d[i[0]].append(i[1])
        except KeyError:
            d[i[0]] = [i[1]]
    s = ''
    if align_results:
        p -= 1
    else:
        p = 0
    ic = 1
    for i in c:
        if str(ic) in d.keys():
            m = re.match(e, i) 
            s += m.group(1).rstrip().ljust(p) + ' #= ' 
            while d[str(ic)]:
                s += (d[str(ic)].pop(0).encode('utf8') + b', ').decode('utf8')  # insert result
            s = s[:-2]  # remove last comma and space
            if '#' in m.group(3):
                s += '  # ' + m.group(3).split('#', 1)[1].strip()  # insert eventual comments after result
        elif 'import hashequal' in i:
            s += i.split('#')[0].rstrip() + '  # run ' + str(datetime.datetime.utcnow()).split('.')[0] + ' UTC'  # insert run time on import hashequal line
        else:
            s += i          
        s += '\n'
        ic += 1
    open(f, 'w').write(s[:-1])  # overwrite original script with annotated file

# remove modified script and prevent execution of orginal script
os.remove(t)
exit()
