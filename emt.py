__author__ = "Winter"

import configparser
import os
import subprocess
from codecs import decode

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
        if config_option_name in ["repo_dir","dev_dir","bat_path","makepbo_dir","a3_dir","a3_miss"]:
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
    check_config_option("ArmA 3 Directory","a3_dir","Example: C:\Program Files (x86)\Steam\SteamApps\common\Arma 3")
    check_config_option("ArmA 3 Profile Name","a3_prof","Example: IamNotDyslexci")
    check_config_option("ArmA 3 Mission Path","a3_miss","Example: G:\Documents\Arma 3 - Other Profiles\Profile\missions\Dev.stratis\mission.sqm")
    check_config_option("MakePBO","makepbo_dir","Example: C:\Program Files (x86)\Mikero\DePboTools\bin")
    check_config_option("Mod Name","mod_name","Example: myaddon")
    check_config_option("Repository Directory","repo_dir","Example: G:\Arma\Modset")
    check_config_option("Mod Dev Directory","dev_dir","Example: G:\Arma\Dev\myaddon") # currently needs to point at specific mod

def get_config_option(config_option_name):
    config.read(config_file)
    return config.get("main",config_option_name)

def clear_old_mod(mod_dir,pbo):
    print(mod_dir)
    current_files = os.listdir(mod_dir)
    print("Files in the Repository directory: {}".format(current_files))
    if pbo in current_files:
        print("Removing the old {}...".format(pbo))
        os.remove(os.path.join(mod_dir,pbo))
    else:
        print("{} is not present in the repository".format(pbo))

def check_dev_dir(dev_dir,mod_name):
    current_files = os.listdir(dev_dir)
    print("Files in the Dev directory: {}".format(current_files))
    if "config.cpp" in current_files:
        print("A config.cpp file was found in the dev directory")
        return True
    else:
        print("A config.cpp file was not found in the dev directory")
        return False

def path_list():
    return (os.environ['PATH']).split(";")

def check_makepbo(makepbo_path):
    print("Checking if MakePBO is present...")
    # trying in the PATH variable first
    if makepbo_path in path_list():
        print("Mikero's Tools are present in the PATH variable")
        return True
    else:
        print("Mikero's Tools are not in the PATH variable")

        return False

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

def make_mod_dirs_list(repo_dir):
    print("Building Mod Directory List...")
    mod_dir_seperator = ";"
    mod_list = ""
    for mod in os.listdir(repo_dir):
        mod_directory = os.path.join(repo_dir,mod)
        mod_list += (mod_directory + mod_dir_seperator)
    print("Mod Directory List: {}".format(mod_list))
    return mod_list

def start_arma(a3_path,a3_prof,a3_miss,repo_dir):
    # ArmA has to know about anything in the repo dir, because of dependencies like CBA
    a3_path = os.path.join(a3_path,"arma3.exe") # adding arma3.exe to the end of the path
    mods_used = "-mod=" + make_mod_dirs_list(repo_dir)
    world = "-world=empty"
    arguments = [a3_path, mods_used, a3_prof, world, "-noSplash","-noFilePatching","-showscripterrors",a3_miss]
    try:
        process = subprocess.Popen(arguments)
    except subprocess.CalledProcessError as error:
        output = process.communicate()[0]
        print(process.returncode)
        print("ArmA 3 didn't manage to start!")
    else:
        print("ArmA 3 successfully started")

config_file = "settings.ini"
# init config
config = configparser.ConfigParser()
# check config's existence
check_configs()
# check if makepbo is present
check_makepbo(get_config_option("makepbo_dir"))
# set globals
arma3_directory = get_config_option("a3_dir")
arma3_profile_name = get_config_option("a3_prof")
arma3_mission_path = get_config_option("a3_miss")
repository_directory = get_config_option("repo_dir")
mod_name = get_config_option("mod_name")
mods_directory = os.path.join(repository_directory,"@" + mod_name,"addons")
pbo_name = mod_name + ".pbo"
pbo_path = os.path.join(mods_directory,pbo_name)
dev_directory = get_config_option("dev_dir")
# clear old pbo
clear_old_mod(mods_directory,pbo_name)
# try to pack the pbo
if try_to_pack_pbo(mods_directory,dev_directory,mod_name):
    # if pbo is fine, try to start arma
    start_arma(arma3_directory,arma3_profile_name,arma3_mission_path,repository_directory)