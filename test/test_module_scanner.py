# Fix error module not found
import os
import sys
sys.path.append(os.getcwd())

from jagad.handler.module import Manager
from jagad.exceptions import NoModuleError

manager = Manager()
manager.initalize()
while True:
    s = input("Search: ")
    if s == "exit": break
    else:
        print (manager.exists(s))