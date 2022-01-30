import os
import sys
sys.path.append(os.getcwd())

from jagad.utils.time import get_timenow
from jagad.utils.time import FORMAT_GET_TIME, FORMAT_CALENDAR, FORMAT_FULL

print (get_timenow(FORMAT_FULL))