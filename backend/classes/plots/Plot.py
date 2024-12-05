from abc import ABC


class Plot(ABC):
    def __init__(self, input_data=None, isSaved=False):
        self.input_data = input_data
        self.name = "Template"

        self.isSaved = isSaved

    def plot(self):
        # print("Plotting {}".format(self.name))
        pass

