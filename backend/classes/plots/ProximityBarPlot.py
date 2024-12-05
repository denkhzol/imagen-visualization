from .Plot import Plot


class ProximityBarPlot(Plot):

    def __init__(self, input_data,  isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "ProximityBarPlot"


    def plot(self):
        super().plot()

        desired_animal_list, proximity, radius = self.input_data
        animal_indices = []
        for animal in desired_animal_list:
            animal_indices.append(animal.id[0])
        data = {
            "x": animal_indices,
            "y": proximity,
            "type": "bar"
        }

        return {"title": 'proximityBar', "data_list": data}


