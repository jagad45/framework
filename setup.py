import sys
import subprocess
import pkg_resources

try:
    import platform
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "platform"], stdout=subprocess.DEVNULL)
try:
    import requests
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "requests"], stdout=subprocess.DEVNULL)

print ("[!] No implemented script!")