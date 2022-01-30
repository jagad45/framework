import os
import sys
sys.path.append(os.getcwd())

from jagad.net.downloader import Downloader

geckodriver_url = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"
downloader = Downloader()
downloader.download(geckodriver_url, filename="geckodriver.tar.gz")