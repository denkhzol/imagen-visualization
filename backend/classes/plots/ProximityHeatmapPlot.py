from .Plot import Plot


class ProximityHeatmapPlot(Plot):

    def __init__(self, input_data, isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "ProximityHeatmapPlot"

    def plot(self):
        super().plot()

        animal_matrix, radius = self.input_data

        return {"title": 'ProximityHeatmap', "z": animal_matrix.tolist(), 'type': 'heatmap'}
