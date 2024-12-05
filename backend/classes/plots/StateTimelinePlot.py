import sys
from .Plot import Plot


class StateTimelinePlot(Plot):

    def __init__(self, input_data, isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "StateTimelinePlot"

    def plot(self):
        super().plot()

        animals, selected_animal_id = self.input_data

        founded = 0
        for animal in animals:
            if animal.id[0] == selected_animal_id:
                selected_animal = animal
                founded = 1
        if founded == 0:
            print("the animal not found")
            sys.exit()
        concrete_states = selected_animal.concrete_states

        frame_count = len(animals[0].x)

        sitting = []
        moving = []
        eating = []

        for frame in range(frame_count):
            if concrete_states[frame] == "sitting":
                sitting.append(frame)
            if concrete_states[frame] == "moving":
                moving.append(frame)
            if concrete_states[frame] == "eating":
                eating.append(frame)

        data_sitting = []
        if len(sitting) > 0:
            sitting_ranges = []
            sitting_start = sitting[0]

            for i in range(1, len(sitting)):
                # Check if current element is not consecutive with the previous one
                if sitting[i] != sitting[i - 1] + 1:
                    # End of a sequence
                    sitting_ranges.append([sitting_start-0.1, sitting[i - 1]+0.1])
                    # Start a new sequence
                    sitting_start = sitting[i]

            # Append the last sequence
            sitting_ranges.append([sitting_start-0.1, sitting[-1]+0.1])
            for i in range(len(sitting_ranges)):
                data = {
                    "x": sitting_ranges[i],
                    "y": ["sitting", "sitting"],
                    "mode": "lines",
                    "name": "sitting"
                }
                data_sitting.append(data)

        data_moving = []
        if len(moving) > 0:
            moving_ranges = []
            moving_start = moving[0]

            for i in range(1, len(moving)):
                # Check if current element is not consecutive with the previous one
                if moving[i] != moving[i - 1] + 1:
                    # End of a sequence
                    moving_ranges.append([moving_start-0.1, moving[i - 1]+0.1])
                    # Start a new sequence
                    moving_start = moving[i]

            # Append the last sequence
            moving_ranges.append([moving_start-0.1, moving[-1]+0.1])
            for i in range(len(moving_ranges)):
                data = {
                    "x": moving_ranges[i],
                    "y": ["moving", "moving"],
                    "mode": "lines",
                    "name": "moving"
                }
                data_moving.append(data)

        data_eating = []
        if len(eating) > 0:
            eating_ranges = []
            eating_start = moving[0]

            for i in range(1, len(eating)):
                # Check if current element is not consecutive with the previous one
                if eating[i] != eating[i - 1] + 1:
                    # End of a sequence
                    eating_ranges.append([eating_start-0.1, eating[i - 1]+0.1])
                    # Start a new sequence
                    eating_start = eating[i]

            # Append the last sequence
            eating_ranges.append([eating_start-0.1, eating[-1]+0.1])
            for i in range(len(eating_ranges)):
                data = {
                    "x": eating_ranges[i],
                    "y": ["eating", "eating"],
                    "mode": "lines",
                    "name": "eating"
                }
                data_eating.append(data)

        return {"title": 'StateTimeLine', "data_moving": data_moving, "data_sitting": data_sitting,
                "data_eating": data_eating}
