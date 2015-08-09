__author__ = "Winter"

from datetime import datetime
from evergreen import configuration
import os
import winshell
import subprocess

MAKEPBO_FILE_NAME = "makepbo.exe"
CONFIG_FILE_NAME = "settings.ini"
CURRENT_TIME = datetime.now().time()
CURRENT_TIME_STR = str(CURRENT_TIME)
CURRENT_DATE = datetime.now().date()
CURRENT_DATE_STR = str(CURRENT_DATE)

def main():
    config_file = "settings.ini"
    # init a configuration instance
    evergreen = configuration(CONFIG_FILE_NAME)
    settings_instance = evergreen.open_instance()
    # write the metadata
    evergreen.write_meta_data(settings_instance, CURRENT_DATE_STR, CURRENT_TIME_STR)
    # check if config options are all present
    settings_required = [
        ['directories', 'game_dir'],
        ['directories', 'makepbo_dir'],
        ['directories', 'repo_dir'],
        ['directories', 'mod_dev_dir'],
        ['paths', 'mission_path'],
        ['settings', 'profile_name'],
        ['settings', 'mod_name']
    ]
    for section, option in settings_required:
        evergreen.check_value(settings_instance, section, option)
    # set global variables
    arma_game_directory = evergreen.return_value(settings_instance, 'directories', 'game_dir')
    makepbo_dir = evergreen.return_value(settings_instance, 'directories', 'makepbo_dir')
    mod_repository_directory = evergreen.return_value(settings_instance, 'directories', 'repo_dir')
    mod_development_directory = evergreen.return_value(settings_instance, 'directories', 'mod_dev_dir')
    arma_mission_path = evergreen.return_value(settings_instance, 'paths', 'mission_path')
    arma_profile_name = evergreen.return_value(settings_instance, 'settings', 'profile_name')
    arma_mod_name = evergreen.return_value(settings_instance, 'settings', 'mod_name')
    # is makepbo present?
    print('Checking for MakePBO')
    # check in the path list
    path_list = (os.environ['PATH']).split(';')
    print_list('PATH list:', path_list)
    if makepbo_dir in path_list:
        print('MakePBO is present in the PATH list')
    else:
        print('MakePBO is not present. Install it!')
        return -1
    # setup the pbo name
    pbo_file = arma_mod_name + ".pbo"
    # remove the old pbo
    print(r'Checking the mod directory for the old pbo')
    current_mods = os.listdir(mod_repository_directory)
    print_list('Current mods:', current_mods)
    if pbo_file in current_mods:
        pbo_path = os.path.join(mod_repository_directory, pbo_file)
        print(r'Mod found at the path: {}'.format(pbo_path))
        print('Removing old mod pbo')
        winshell.delete_file(pbo_path, no_confirm=True)
    else:
        print('There is no old version of the mod in the repository')


def print_list(prompt='', list=[]):
    print(prompt)
    for element in list:
        print('\t{}'.format(element))
"""
    # try to pack the pbo
    if try_to_pack_pbo(mods_directory,dev_directory,mod_name):
        # if pbo is fine, try to start arma
        start_arma(arma3_directory,arma3_profile_name,arma3_mission_path,repository_directory)


# checks if an option (example: repo_dir) is present in the config and if not, asks for the value
def check_config_option(config_file, option_name,config_option_name,example_prompt):
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



def get_config_option(config_option_name):
    config.read(config_file)
    return config.get("main",config_option_name)

def check_dev_dir(dev_dir,mod_name):
    current_files = os.listdir(dev_dir)
    print("Files in the Dev directory: {}".format(current_files))
    if "config.cpp" in current_files:
        print("A config.cpp file was found in the dev directory")
        return True
    else:
        print("A config.cpp file was not found in the dev directory")
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
    a3_path = os.path.join(a3_path,"arma3.exe") # adding arma3.exe to the end of the path
    # ArmA has to know about anything in the repo dir, because of dependencies like CBA
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
"""
if __name__ == "__main__":
    main()