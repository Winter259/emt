__author__ = "Winter"

import configparser
import os
import subprocess

# check if settings.ini exists
def check_config_existence(config_file):
    if not os.path.exists(config_file):
        print("settings.ini is not present, deploying one now...")
        configfile = open("\\" + config_file,"w")
        config.add_section("main")
        with open(config_file,"w") as configfile:
            config.write(configfile)
        print("Successfully deployed new settings.ini: {}".format(os.path.exists(config_file)))
    else:
        print("settings.ini is present")

# checks if an option (example: repo_dir) is present in the config and if not, asks for the value
def check_config_option(option_name,config_option_name,example_prompt):
    config.read(config_file)
    try:
       config.get("main",config_option_name)
    except configparser.NoOptionError:
        print("{} is not present in settings.ini".format(option_name))
        print("Please enter a value for: {}".format(option_name))
        print(example_prompt)
        new_option_value = input("Input: ")
        if config_option_name in ["repo_dir","dev_dir","bat_path"]:
            while not os.path.exists(new_option_value):
                new_option_value = input("That directory does not exist! Please enter a valid directory: ")
        config.set("main",config_option_name,new_option_value)
        with open(config_file,"w") as configfile:
            config.write(configfile)
        print("{} is now: {}".format(option_name,config.get("main",config_option_name)))
    else:
        print("{} is: {}".format(option_name,config.get("main",config_option_name)))

def check_configs():
    check_config_existence(config_file)
    check_config_option("MakePBO","makepbo_path","Example: C:\Program Files (x86)\Mikero\DePboTools\\bin")
    check_config_option("Mod Name","mod_name","Example: myaddon")
    check_config_option("Repository Directory","repo_dir","Example: G:\Arma\Modset\@Mod\\addons")
    check_config_option("Mod Dev Directory","dev_dir","Example: G:\Arma\Dev\myaddon") # currently needs to point at specific mod
    check_config_option("Bat File Path","bat_path","Example: G:\Arma\Dev\mybatfile.bat")

def get_config_option(config_option_name):
    config.read(config_file)
    return config.get("main",config_option_name)

def clear_old_mod(repo_dir,pbo):
    current_files = os.listdir(repo_dir)
    print("Files in the Repository directory: {}".format(current_files))
    if pbo in current_files:
        print("Removing old {}...".format(pbo))
        os.remove(repo_dir + "\\" + pbo)
    else:
        print("{} is not present in the repository".format(pbo))

def check_dev_dir(dev_dir,mod_name):
    current_files = os.listdir(dev_dir)
    print("Files in the Dev directory: {}".format(current_files))
    if "config.cpp" in current_files:
        print("A config.cpp file was present in the dev directory")
        return True
    else:
        print("A config.cpp file was not present in the dev directory")
        return False

def path_list():
    return (os.environ['PATH']).split(";")

def check_makepbo(makepbo_path):
    print("Checking if MakePBO is present...")
    print(path_list())
    if makepbo_path in path_list():
        print("Mikero's Tools are present in the PATH variable")
        return True
    else:
        print("Mikero's Tools are not in the PATH variable")

def try_to_pack_pbo(repo_dir,dev_dir,mod_name):
    if check_dev_dir(dev_dir,mod_name):
        pack_new_pbo(dev_dir,repo_dir)
        return True
    else:
        print("Something went wrong with the directories") # TODO: Replace and make optional
        return False

def pack_new_pbo(dev_repo,repo_dir):
    try:
        #subprocess.check_output(["MakePBO","-P","-A","-L","-N","-G", dev_repo,repo_dir])
        subprocess.check_output(["MakePBO","-P","-A","-L","-N","-G", dev_repo,repo_dir], stderr=subprocess.STDOUT)
    except:
        print("MakePBO broke!")
    else:
        print("New PBO successfully packaged.")

def start_arma(bat_path):
    print("Attempting to run the batch file to start A3...")
    p = subprocess.Popen(bat_path, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()

config_file = "settings.ini"
# init config
config = configparser.ConfigParser()
# check config's existence
check_configs()
# check if makepbo is present
check_makepbo(get_config_option("makepbo_path"))
# set globals
repository_directory = get_config_option("repo_dir")
mod_name = get_config_option("mod_name")
pbo_name = mod_name + ".pbo"
pbo_path = repository_directory + "\\" + pbo_name
dev_directory = get_config_option("dev_dir")
batch_file_path = get_config_option("bat_path")
# clear old pbo
clear_old_mod(repository_directory,pbo_name)
# pack pbo
if try_to_pack_pbo(repository_directory,dev_directory,mod_name):
    start_arma(batch_file_path)