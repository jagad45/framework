import os

def run():
    cmd = ("cls" if os.name == "nt" else "clear")
    os.system(cmd)

if __name__ == "__main__":
    run()