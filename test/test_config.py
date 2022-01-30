import os
import sys
sys.path.append(os.getcwd())

from jagad.utils.config import Config

config = Config()
selector = config.read()
user = selector.select("x")
print (user)