# hashequal
a Python module to write quasi-interactive math sheets  
on execution it modifies the calling script annotating the results of the operations marked with #= 

## example

before running

~~~python
#! /usr/bin/env python

import hashequal

a = 1 + 1 #=
b = a * 2 #=  # comment
~~~

after running

~~~python
#! /usr/bin/env python

import hashequal  # run 2018-11-06 18:59:54 UTC

a = 1 + 1 #= 2
b = a * 2 #= 4  # comment
~~~

## instructions

- import *hashequal* at the beginning of the file, eventually just below the interpreter directive
- mark every operation whose result is to be annotated with a #= comment
- if there need to be further comments on a #= line, use another following #
- do not use the variable *hashequal_data*: it is used by the module for handling the results

## options

edit hashequal.py to set

~~~python
align_results = True  # if True all the results are aligned to the rightmost #=
~~~
