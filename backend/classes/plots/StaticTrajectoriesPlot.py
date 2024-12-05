from .Plot import Plot


class StaticTrajectoriesPlot(Plot):

    def __init__(self, input_data, isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "StaticTrajectoriesPlot"

    def plot(self):
        super().plot()
        desired_animal_list = self.input_data
        animal_type = desired_animal_list[0].type

        data_list = []

        for animal in desired_animal_list:
            data = {
                "name": str(animal.type) + str(animal.id[0]),
                "x": animal.x.tolist(),
                "y": animal.y.tolist(),
                "mode": "lines",
                "type": "scatter"
            }
            data_list.append(data)
        return {"title": 'StaticTrajectory', "data_list": data_list}


