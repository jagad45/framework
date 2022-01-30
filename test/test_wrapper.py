# Fix error module not found
import os
import sys
sys.path.append(os.getcwd())

from jagad.utils.wrapper import wrap_string

data = "Hello, my name is Billal Fauzan, i'm from Majalengka, my facebook account is billal.xcode.123"
print (wrap_string(data, indent=2, indentAll=True))