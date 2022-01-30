import requests
import signal
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from typing import Iterable
from threading import Event
from urllib.request import urlopen
from urllib.parse import urlparse
from jagad.terminal.console import print, print_warning, print_error
from jagad.utils.constants import ROOT_PATH
from jagad.net.useragent import choice_random as useragent_random
from pathlib import Path
try:
    from rich.progress import (
        BarColumn,
        DownloadColumn,
        Progress,
        TaskID,
        TextColumn,
        TimeRemainingColumn,
        TransferSpeedColumn,
    )
except ModuleNotFoundError:
    print_error("No module 'rich' found!", _quit=True)

class PathError(Exception):
    def __init__(self, message) -> None:
        self.message = message

def check_path_exists(path, makedir=True, force_makedir=False):
    path = Path(path)
    parent_path = path.parent
    parents_path = [parent for parent in path.parents]
    if os.path.isdir(parent_path):
        if os.path.isdir(path): return True
        elif os.path.isfile(path):
            if makedir and force_makedir:
                path.mkdir(parents_path[-1])
                return True
            else: raise PathError("Is a directory")
        else:
            if makedir:
                path.mkdir(parents_path[-1])
                return True
            else:
                raise PathError("No path found")
    else:
        raise PathError("No path parent found")

class Downloader:
    def __init__(self) -> None:
        self.PATH = os.path.join(ROOT_PATH, "downloader")
        self.session = requests.Session()
        self.headers = {}
        self.stream = False

        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        self.done_event = Event()

    def check_path_exists(self):
        try:
            if check_path_exists(self.PATH): return True
        except PathError as err:
            print_error(err.message, _quit=True)

    def ask_filename(self):
        user_filename = input("[?] Input filename: ")
        return user_filename

    def ask_overwrite(self):
        user_input = input("[?] Overwrite file? (Y/n): ")
        if user_input.strip() == "" or user_input.lower() == "y": return True
        else: return False

    def handle_sigint(self, signum, frame):
        self.done_event.set()

    def set_stream(self, v: bool):
        if isinstance(v, bool):
            self.stream = v
        else:
            raise ValueError

    def set_useragent(self, useragent: str):
        self.headers["user-agent"] = useragent

    def build_header(self):
        if "user-agent" not in self.headers:
            self.headers["user-agent"] = useragent_random()

    def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
        """Copy data from a url to a local file."""
        response = urlopen(url)
        # This will break if the response doesn't contain content length
        self.progress.update(task_id, total=int(response.info()["Content-length"]))
        with open(path, "wb") as dest_file:
            self.progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                self.progress.update(task_id, advance=len(data))
                if self.done_event.is_set():
                    return

    def download(self, url: str, filename: str = None, progess_type="rich", progress_active=True):
        self.check_path_exists()
        if filename is None or filename == "":
            path = urlparse(url).path
            if path == "":
                user_filename = self.ask_filename()
                filename = os.path.join(self.PATH, user_filename)
            else:
                if "/" in path:
                    slash_split = path.split("/")
                    filename_endslash = slash_split[-1]
                    filename = os.path.join(self.PATH, filename_endslash)
                else:
                    user_filename = self.ask_filename()
                    filename = os.path.join(self.PATH, user_filename)
        else:
            filename = os.path.join(self.PATH, filename)

        if os.path.isfile(filename):
            if self.ask_overwrite() is True: pass
            else: return False
        
        with self.progress:
            with ThreadPoolExecutor(max_workers=4) as pool:
                task_id = self.progress.add_task("download", filename=filename.split("/")[-1], start=False)
                pool.submit(self.copy_url, task_id, url, filename) 