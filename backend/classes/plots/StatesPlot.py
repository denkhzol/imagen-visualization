from .Plot import Plot


class StatesPlot(Plot):

    def __init__(self, input_data,  isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "StatesPlot"


    def plot(self):
        super().plot()

        animals = self.input_data
        ids = []
        ones = []

        eating = [0 for animal in animals]
        moving = [0 for animal in animals]
        sitting = [0 for animal in animals]

        frame_count = len(animals[0].x)

        for animal in animals:
            ids.append(animal.id[0])
            ones.append(1)

        for animal in animals:
            id_ = animal.id[0]-1
            for frame in range(frame_count):
                state = animal.concrete_states[frame]
                if state == "eating":
                    eating[id_] += 1
                if state == "moving":
                    moving[id_] += 1
                if state == "sitting":
                    sitting[id_] += 1

        sitting = [a for a in sitting]
        moving = [a for a in moving]
        eating = [a for a in eating]

        data_sitting = {
            "x": ids,
            "y": sitting,
            "name": "sitting",
            "type": "bar"
        }
        data_moving = {
            "x": ids,
            "y": moving,
            "name": "moving",
            "type": "bar"
        }
        data_eating = {
            "x": ids,
            "y": eating,
            "name": "eating",
            "type": "bar"
        }

        return {"title": 'StatePlot', "data_sitting": data_sitting, "data_eating": data_eating,
                "data_moving": data_moving,
}
