from .Plot import Plot


class DistanceBarPlot(Plot):

    def __init__(self, input_data, isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "DistanceBarPlot"

    def plot(self):
        super().plot()

        desired_animal_list = self.input_data

        animal_type = desired_animal_list[0].type

        distances = []
        ids = []

        for animal in desired_animal_list:
            distances.append(animal.distance)
            ids.append(animal.id[0])

        return {"title": 'distanceBar', "x": ids, "y": distances, "type": "bar"}
