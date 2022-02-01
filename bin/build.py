#!/usr/bin/env python3
import os
import sys
import shutil

try:
    import pathlib
except (ImportError, ModuleNotFoundError):
    print (f"[!] Module 'pathlib' not found, please see instructure installer")
    sys.exit()

def print(text):
    sys.stdout.write(f"[INFO]: {text}\n")
    sys.stdout.flush()

def print_error(text):
    sys.stdout.write(f"[ERROR]: {text}\n")
    sys.stdout.flush()

def print_list(obj):
    if isinstance(obj, list) is False:
        raise ValueError
    for index, item in enumerate(obj):
        sys.stdout.write(f"  {index + 1}). {item}\n")
        sys.stdout.flush()

def user_input(text):
    undefined = input(f"[?] {text}")
    return undefined

class Builder:
    def __init__(self) -> None:
        self.build_path = os.path.join(os.getcwd(), "build")
        self.python_environments = ""
        self.package_path = ""

    def create_build_dir(self):
        if os.path.isdir(self.build_path):
            user_tchoice = user_input(f"Delete old build dir? (Y/n): ")
            if user_tchoice.lower() == "y":
                shutil.rmtree(self.build_path)
                print("Success delete old dir")
                return self.create_build_dir()
            else:
                sys.exit()
        else:
            print("Make new build dir")
            try:
                os.mkdir(self.build_path)
                return True
            except OSError:
                return self.create_build_dir()

    def read_requirements(self):
        requirements_path = os.path.join(os.getcwd(), "requirements.txt")
        if os.path.isfile(requirements_path) is False:
            requirements_path = os.path.join(os.getcwd(), "..", "requirements.txt")
            if os.path.isfile(requirements_path) is False:
                sys.exit("[ERROR]: No such requirements file.")
        
        requirements = []
        with open(requirements_path, "r") as File:
            content_line = File.read().splitlines()
            for content in content_line:
                content_split = content.split("==")
                temp = {}
                temp["name"] = content_split[0]
                temp["version"] = None
                if len(content_split) == 2:
                    temp["version"] = content_split[1]
                requirements.append(temp)
        return requirements

    def choice_python_library_path(self, path: str):
        python_environments = ""
        temp = [os.path.join(path, x) for x in os.listdir(path) if "python" in x]
        if len(temp) == 0:
            print_error("No python environment found")
            while True:
                python_environments = user_input("Paste python path: ")
                if os.path.isdir(python_environments) is False: pass
                else: break
        else:
            print_list(temp)
            while True:
                python_choice = user_input("Choice python: ")
                if python_choice.isdigit():
                    python_choice_number = int(python_choice) - 1
                    if python_choice_number > len(temp):
                        print("Please choice a number")
                    else:
                        temp_path = temp[python_choice_number]
                        if os.path.isfile(temp_path):
                            print("This path is a file")
                        elif os.path.isdir(temp_path):
                            python_environments = temp_path
                            break
                        else:
                            print ("No such file or directory")
                else:
                    print("Please choice a number")
        
        print (f"Your select python path: {python_environments}")
        self.python_environments = python_environments
        return True

    def check_site_dist_packages(self):
        if self.python_environments == "":
            print_error("No python environment.")
            sys.exit()
        else:
            packages = ["dist-packages", "site-packages"]
            tempackage = []
            for package in packages:
                python_join_path = os.path.join(self.python_environments, package)
                if os.path.isdir(python_join_path):
                    print(f"Found {package} on {self.python_environments}")
                    tempackage.append(package)
            if len(tempackage) == 0:
                print_error("No package found on environments.")
                sys.exit()
            elif len(tempackage) == 1:
                self.package_path = tempackage[0]
            else:
                print_list(tempackage)
                while True:
                    package_choice = user_input("Choice package: ")
                    if package_choice.isdigit():
                        package_choice_number = int(package_choice) - 1
                        if package_choice_number > len(tempackage):
                            print("Please choice a number")
                        else:
                            temp_path = tempackage[package_choice_number]
                            if os.path.isfile(temp_path):
                                print("This path is a file")
                            elif os.path.isdir(temp_path):
                                self.package_path = temp_path
                                break
                            else:
                                print ("No such file or directory")
                    else:
                        print("Please choice a number")

    def copy_library_build_dir(self):
        looping = True
        while looping:
            library_path = input("[?] Paste here library path: ")
            if os.path.isdir(library_path):
                requirements = self.read_requirements()
                looping = False
            else:
                print ("No such file or directory")
        
        if len(requirements) == 0:
            print ("No requirements found!")
            sys.exit()
        else:
            if self.choice_python_library_path(library_path):
                self.check_site_dist_packages()

if __name__ == "__main__":
    try:
        apps = Builder()
        apps.create_build_dir()
        apps.copy_library_build_dir()
    except:
        sys.exit("User quit")