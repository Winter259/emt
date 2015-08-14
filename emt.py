__author__ = "Winter"

from time import sleep
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
        ['paths', 'server_config'],
        ['settings', 'profile_name'],
        ['settings', 'mod_name'],
        ['settings', 'mod_container_name'],
        ['settings', 'arma_exe'],
        ['settings', 'misc_client_params'],
        ['settings', 'launch_dedi']
    ]
    for section, option in settings_required:
        evergreen.check_value(settings_instance, section, option)
    # set global variables
    game_directory = evergreen.return_value(settings_instance, 'directories', 'game_dir')
    makepbo_dir = evergreen.return_value(settings_instance, 'directories', 'makepbo_dir')
    mod_repository_directory = evergreen.return_value(settings_instance, 'directories', 'repo_dir')
    mod_development_directory = evergreen.return_value(settings_instance, 'directories', 'mod_dev_dir')
    mission_path = evergreen.return_value(settings_instance, 'paths', 'mission_path')
    server_config_path = evergreen.return_value(settings_instance, 'paths', 'server_config')
    profile_name = evergreen.return_value(settings_instance, 'settings', 'profile_name')
    mod_name = evergreen.return_value(settings_instance, 'settings', 'mod_name')
    mod_container_name = evergreen.return_value(settings_instance, 'settings', 'mod_container_name')
    executable_name = evergreen.return_value(settings_instance, 'settings', 'arma_exe')
    misc_client_params = evergreen.return_value(settings_instance, 'settings', 'misc_client_params')
    launch_dedicated_server = evergreen.return_value(settings_instance, 'settings', 'launch_dedi')
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
    pbo_file = mod_name + ".pbo"
    # remove the old pbo
    print(r'Checking the mod directory for the pbo: {}'.format(pbo_file))
    pbo_dir = os.path.join(mod_repository_directory, mod_container_name, 'addons')
    pbo_dir_contents = os.listdir(pbo_dir)
    pbo_path = os.path.join(pbo_dir, pbo_file)
    print_list('Current mods in the mod container folder:', pbo_dir_contents)
    if pbo_file in pbo_dir_contents:
        print(r'Mod found at the path: {}'.format(pbo_path))
        print('The old m')
        winshell.delete_file(pbo_path, no_confirm=True)
    else:
        print('There is no old version of the mod in the repository')
    # pack the pbo using makepbo
    try:
        subprocess.check_output(['MakePBO', '-P', '-A', '-L', '-N', '-G', mod_development_directory, pbo_dir], stderr=subprocess.STDOUT)
    except Exception as e:
        print('MakePBO broke! It raised the exception: {}'.format(e))
        return -1
    else:
        print('New PBO successfully packaged.')
    # produce a list of mods to run from the whole contents of the repository
    repo_contents = os.listdir(mod_repository_directory)
    if len(repo_contents) > 0:
        addon_params_string = ''
        addon_separator = ';'
        print('Building a list of addons to launch with arma')
        for addon in repo_contents:
            print('\tAdding: {} to the list of addons'.format(addon))
            addon_directory = os.path.join(mod_repository_directory, addon)
            addon_params_string += (addon_directory + addon_separator)
    else:
        print('There are no mods present inside the repository!')
        return -1
    executable_path = os.path.join(game_directory, executable_name)
    mods_used_parameter = '-mod=' + addon_params_string
    world_param = '-world=empty'
    profile_param = '-name=' + profile_name
    client_params = misc_client_params.split(' ')
    client_start_arguments = [executable_path, profile_param, mods_used_parameter, world_param]
    client_start_arguments.extend(client_params)
    if int(launch_dedicated_server) == 1:
        server_executable_path = os.path.join(game_directory, 'arma3sever.exe')
        config_param = '-config=' + server_config_path
        server_start_arguments = [server_executable_path, config_param, mods_used_parameter]
        print_list('Starting ArmA dedicated server using the following parameters:', server_start_arguments)
        try:
            process = subprocess.Popen(server_start_arguments)
        except subprocess.CalledProcessError as error:
            print("ArmA 3 Server didn't manage to start!")
            output = process.communicate()[0]
            print(process.returncode)
        else:
            print("ArmA 3 Dedicated Server successfully started")
            pause('Waiting 10 seconds for the server to start up', 10)
            client_start_arguments.append('-connect=127.0.0.1')  # make client connect to the dedicated server
    else:
        print('Starting ArmA in editor')
        client_start_arguments.append(mission_path)
    print_list('Starting ArmA client using the following parameters:', client_start_arguments)
    try:
        process = subprocess.Popen(client_start_arguments)
    except subprocess.CalledProcessError as error:
        print("ArmA 3 didn't manage to start!")
        output = process.communicate()[0]
        print(process.returncode)
    else:
        print("ArmA 3 successfully started")

def print_list(prompt='', list=[]):
    print(prompt)
    for element in list:
        print('\t{}'.format(element))

def pause(prompt='', time=10):
    count = time
    while count > 0:
        print('{}: {}'.format(count, prompt))
        sleep(1)
        count -=1

if __name__ == "__main__":
    main()