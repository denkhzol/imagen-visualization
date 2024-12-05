import yaml
class ConfigurationManager(object):
    """
    To read configuration parameters from specified config file (.yml)

    Parameters
    ----------

    location: path
        Path to the configuration file.
    """

    def __init__(self, location, abs_path):
        try:
            self.__load_configuration(location)
        except FileNotFoundError:
            # try to find the file in root of project
            local_location = abs_path / location
            self.__load_configuration(local_location)
        # print("Current configuration:")
        # print(self.__configuration)

    def __load_configuration(self, location):
        with open(location, 'r') as yamlfile:
            self.__configuration = yaml.load(yamlfile, Loader=yaml.FullLoader)

    @property
    def configuration(self):
        return self.__configuration
