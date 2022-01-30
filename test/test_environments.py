import os
import sys
sys.path.append(os.getcwd())

from jagad.environments import Environments, Selector

env = Environments()
env.run()

selector = Selector(env)
while True:
    try:
        x = input("Enter: ")
        splt = x.split(" ")
        if splt[0] == "insert":
            key = splt[1]
            val = splt[2]
            selector.insert(key, val)
        elif splt[0] == "delete":
            key = splt[1]
            selector.delete(key)
        elif splt[0] == "all":
            print (selector.get_all)
        elif splt[0] == "exit":
            env.destroy()
            break
        elif splt[0] == "!":
            print (selector.is_connected())
    except KeyboardInterrupt:
        env.destroy()
        break
    