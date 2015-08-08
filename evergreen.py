__author__ = 'Simon'

from os import getcwd
from os.path import join, exists
import configparser

class configuration:
    def __init__(self, file_name, location=getcwd()):
        self.file_name = file_name
        self.location = location
        self.path = join(location, file_name)
        if not exists(self.path):
            config_print('Config does not exist, creating new config')
            self.create_empty_file()
        else:
            config_print('Config already exists')

    def create_empty_file(self):
        config_file = open(self.path, 'w')
        config_file.close()

    def open_instance(self):
        config_instance = configparser.ConfigParser()
        return config_instance

    def return_sections(self, config_instance):
        config_instance.read(self.file_name)
        return config_instance.sections()

    def check_section(self, config_instance, required_section):
        config_instance.read(self.file_name)
        sections = config_instance.sections()
        if required_section in sections:
            return True
        else:
            return False

    def add_section(self, config_instance, new_section):
        config_file = open(self.path, 'w')
        try:
            config_instance.add_section(new_section)
        except configparser.DuplicateSectionError:
            config_print('Section with name: {} already exists in the config: {}'.format(new_section, self.file_name))
        else:
            config_print('Section with name: {} added to the config: {}'.format(new_section, self.file_name))
        finally:
            config_instance.write(config_file)
            config_file.close()

    def return_value(self, config_instance, section, option):
        config_instance.read(self.file_name)
        try:
            option_return = config_instance.get(section, option)
        except configparser.NoSectionError:
            config_print('No option available by the value: {} in the config: {}'.format(option, self.file_name))
            return None
        except configparser.NoOptionError:
            config_print('No option available by the value: {} in the config: {}'.format(option, self.file_name))
            return None
        else:
            config_print('Option return: {} from section: {} in config: {}'.format(option_return, section, self.file_name))
            return option_return

    def set_value(self, config_instance, section, option, value, force_section_make=False):
        if not config_instance.check_section(config_instance, section):
            config_print('The section: {} does not exist within the config: {}'.format(section, self.file_name))
            if force_section_make:
                config_instance.add_section(config_instance, section)
            else:
                config_print('A value could not be set inside a non-existant section (section was not force created)')
                return None
        else:
            config_file = open(self.location, 'w')
            config_instance.set(section, option, value)
            config_instance.write(config_file)
            config_file.close()


def config_print(message=''):
    if evergreen_debug:
        print('[EVERGREEN] {}'.format(message))

def main():
    evergreen = configuration("settings.ini")
    settings_instance = evergreen.open_instance()
    print(evergreen.return_sections(settings_instance))
    evergreen.add_section(settings_instance, 'cats')
    print(evergreen.return_value(settings_instance, 'cats', 'ginger'))

if __name__ == "__main__":
    evergreen_debug = True
    main()
else:
    evergreen_debug = False