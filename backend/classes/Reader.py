import pandas as pd


class Reader(object):
    def __init__(self, configuration, abs_path):
        self.conf = configuration
        self.abs_path = abs_path
        self.data_path = ''
        self.configure()
        self.read()

    def configure(self):
        data_folder = self.conf.configuration["data_folder"]
        data_file = self.conf.configuration["data_file"]

        # TODO fix
        self.data_path = self.abs_path / data_folder / data_file

    def read(self):
        # read the data from the file
        self.df = pd.read_csv(self.data_path, sep=',', names=['Frame',
                                                              'Id',
                                                              'bb_left',
                                                              'bb_top',
                                                              'bb_width',
                                                              'bb_height',
                                                              'conf',
                                                              'x',
                                                              'y',
                                                              ])

        self.__check_data()

        # drop unused columns
        self.df.pop('conf')
        self.df.pop('x')
        self.df.pop('y')

        # generate x and y positions from bounding boxes corners
        self.df['x'] = self.df['bb_left'] + self.df['bb_width'] / 2
        self.df['y'] = self.df['bb_top'] + self.df['bb_height'] / 2

    def __check_data(self):
        pass

    def get_df(self):
        return self.df
