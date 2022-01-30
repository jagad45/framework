# Modul ini berfungsi untuk mengubah teks konstan ke dalam nilai tertentu
from jagad.terminal.colors import Fore

def replace_prompt(s: str, user: str = "", hostname: str = "", path: str = ""):
    keys = {
        "[red]": Fore.RED,
        "[green]": Fore.GREEN,
        "[blue]": Fore.BLUE,
        "[white]": Fore.WHITE,
        "[reset]": Fore.WHITE,
        "[user]": user,
        "[path]": path,
        "[host]": hostname,
        "[hostname]": hostname
    }
    output = s
    while True:
        for item in keys:
            if item in output:
                output.replace(f"{item}", keys[item])
                print (output)
            else: break
    return output