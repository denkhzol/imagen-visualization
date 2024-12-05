from .Plot import Plot
import numpy as np


class VelocityPlot(Plot):

    def __init__(self, input_data,  isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "VelocityPlot"

    def plot(self):
        super().plot()
        animals = self.input_data

        frames = [t for t in range(len(animals[0].x))]

        avg_speed = []
        velocities = []
        ids = []
        text = []
        data_ind = []
        for animal in animals:
            avg_speed.append(animal.avg_v)
            velocities.append(animal.v)
            ids.append(animal.id[0])
            text.append(str(animal.type)+str(animal.id[0]))
            velocities.append(animal.v)

        data_ave = {
            "x": ids,
            "y": avg_speed,
            "mode": 'markers',
            "type": 'scatter',
            "name": 'avg'
        }
        for animal in animals:
            data = {
                "x": frames,
                "y": velocities[animal.id[0]],
                "name": str(animal.id[0]),
                "mode": 'markers',
                "type": 'scatter'
            }
            data_ind.append(data)

        def normal_dist(x, mean, sd):
            prob_density = (1/(np.sqrt(2*np.pi)*sd)) * \
                np.exp(-0.5*((x-mean)/sd)**2)
            return prob_density

        mean_avg_speed = np.mean(avg_speed)
        std_avg_speed = np.std(avg_speed)

        x2 = np.max(avg_speed)
        x = np.linspace(0, x2+10, 100)
        pdf_data = normal_dist(avg_speed, mean_avg_speed, std_avg_speed)
        pdf_fit = normal_dist(x, mean_avg_speed, std_avg_speed)

        a1 = mean_avg_speed-std_avg_speed
        a2 = mean_avg_speed + std_avg_speed
        f1 = normal_dist(a1, mean_avg_speed, std_avg_speed)
        f2 = normal_dist(a2, mean_avg_speed, std_avg_speed)

        data_plot4_dots = {
            "x": avg_speed,
            "y": pdf_data.tolist(),
            "mode": "markers",
            "type": "scatter",
            "name": ""
        }
        data_plot4_line = {
            "x": x.tolist(),
            "y": pdf_fit.tolist(),
            "mode": "lines",
            "type": "scatter",
            "name": ""
        }
        data_plot4_x = {
            "x": [a1, a2],
            "y": [f1, f2],
            "mode": "markers",
            "type": "scatter",
            "name": ""
        }

        data_plot4 = {"data_plot4_line": data_plot4_line, "data_plot4_dots": data_plot4_dots,
                      "data_plot4_x": data_plot4_x}
        flat_velocities = [item for sublist in velocities for item in sublist]
        mean_flat_velocities = np.mean(flat_velocities)
        std_flat_velocities = np.std(flat_velocities)

        x2 = np.max(flat_velocities)
        x = np.linspace(0, x2+10, 100)
        a1 = mean_flat_velocities - std_flat_velocities
        a2 = mean_flat_velocities + std_flat_velocities
        f1 = normal_dist(a1, mean_flat_velocities, std_flat_velocities)
        f2 = normal_dist(a2, mean_flat_velocities, std_flat_velocities)

        pdf2_data = normal_dist(
            flat_velocities, mean_flat_velocities, std_flat_velocities)
        pdf2_fit = normal_dist(x, mean_flat_velocities, std_flat_velocities)

        data_3rd_dots = {
            "x": flat_velocities,
            "y": pdf2_data.tolist(),
            "mode": "markers",
            "type": "scatter",
            "name": ""
        }
        data_3rd_line = {
            "x": x.tolist(),
            "y": pdf2_fit.tolist(),
            "mode": "lines",
            "type": "scatter",
            "name": ""
        }

        data_3rd = {"data_3rd_line": data_3rd_line, "data_3rd_dots": data_3rd_dots}

        return {"title": "VelocityPlot", "IndividualVelocities_data": data_ind, "AverageVelocities_data": data_ave,
                "velocity": data_3rd, "avgVelocity": data_plot4}




