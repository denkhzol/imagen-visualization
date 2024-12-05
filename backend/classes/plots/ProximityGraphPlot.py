from .Plot import Plot
import networkx as nx
import numpy as np


class ProximityGraphPlot(Plot):

    def __init__(self, input_data, isSaved=False):
        super().__init__(input_data, isSaved)
        self.name = "ProximityGraphPlot"

    def plot(self):
        super().plot()
        # self.fig, self.ax = plt.subplots()

        desired_animal_list, animal_matrix, radius = self.input_data
        count = animal_matrix.shape[0]
        animal_type = desired_animal_list[0].type

        G = nx.Graph()
        # Add nodes to the graph
        G.add_nodes_from(range(len(desired_animal_list)))  # Adding 10 nodes (0 to 9)

        # Create a circular layout for nodes
        positions = nx.circular_layout(G)

        # Extract x and y coordinates from the positions
        x = [pos[0] for pos in positions.values()]
        y = [pos[1] for pos in positions.values()]

        for i in range(1, count + 1):
            G.add_node(i)

        a, b = animal_matrix.shape

        for i in range(0, a):
            for j in range(0, b):
                if animal_matrix[i, j] > 0:
                    G.add_edge(i + 1, j + 1, weight=animal_matrix[i, j])
        biggest = np.max(np.max(animal_matrix))

        esmall = [(u, v) for (u, v, d) in G.edges(
            data=True) if d["weight"] < biggest / 3]
        medium = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"]
                  >= biggest / 3 and d["weight"] < biggest * 2 / 3]
        large = [(u, v) for (u, v, d) in G.edges(data=True)
                 if d["weight"] >= biggest * 2 / 3]


        passive = []
        active = []
        eating = []
        very_active = []
        data_nodes = []
        for animal in desired_animal_list:
            if animal.overall_state == 'passive':
                passive.append(animal.id[0])
                data = {
                    "id": animal.id[0],
                    "x": x[animal.id[0]-1],
                    "y": y[animal.id[0]-1],
                    "label": f"Node {animal.id[0]}",
                    "color": "gray"
                }
                data_nodes.append(data)
            if animal.overall_state == 'active':
                active.append(animal.id[0])
                data = {
                    "id": animal.id[0],
                    "x": x[animal.id[0]-1],
                    "y": y[animal.id[0]-1],
                    "label": f"Node {animal.id[0]}",
                    "color": "green"
                }
                data_nodes.append(data)
            if animal.overall_state == 'eating':
                eating.append(animal.id[0])
                data = {
                    "id": animal.id[0],
                    "x": x[animal.id[0]-1],
                    "y": y[animal.id[0]-1],
                    "label": f"Node {animal.id[0]}",
                    "color": "blue"
                }
                data_nodes.append(data)
            if animal.overall_state == 'very_active':
                very_active.append(animal.id[0])
                data = {
                    "id": animal.id[0],
                    "x": x[animal.id[0]-1],
                    "y": y[animal.id[0]-1],
                    "label": f"Node {animal.id[0]}",
                    "color": "red"
                }
                data_nodes.append(data)


        data_edges = []
        for edge in esmall:
            edges = {
                "source": edge[0],
                "target": edge[1],
                "weight": 1
            }
            data_edges.append(edges)
        for edge in medium:
            edges = {
                "source": edge[0],
                "target": edge[1],
                "weight": 2
            }
            data_edges.append(edges)
        for edge in large:
            edges = {
                "source": edge[0],
                "target": edge[1],
                "weight": 2
            }
            data_edges.append(edges)
        return {"title": 'ProximityGraph', "edges": data_edges, "nodes": data_nodes}

