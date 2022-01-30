import os
import sys
sys.path.append(os.getcwd())

from jagad.terminal.shell import Shell

shell = Shell()
shell.initalize()
shell.run()