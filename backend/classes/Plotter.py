from .plots.StaticTrajectoriesPlot import StaticTrajectoriesPlot
from .plots.DistanceBarPlot import DistanceBarPlot
from .plots.ProximityBarPlot import ProximityBarPlot
from .plots.ProximityHeatmapPlot import ProximityHeatmapPlot
from .plots.ProximityGraphPlot import ProximityGraphPlot
from .plots.StatesPlot import StatesPlot
from .plots.VelocityPlot import VelocityPlot
from .plots.StateTimelinePlot import StateTimelinePlot


class Plotter():
    """
    Plotter
    
    This class handles the creation of the Plot objects (needed
    based on the configuration). It also handles the calling of 
    said plots.
    
    Parameters
    ----------
    info : data
        Packaged data required by individual plots.
        Data included in info on this version:
            - desired_animal_list: lists of animals to be plotted
            - image_folder: path to folder including the frames
            - proximity: matrix with proximity information
            - animal_matrix: TODO
            - radius: search radius for specific plots
            - animal: string with the type of animal
            - subject: some plots focus in a single animal, this is the index
    
    abs_path : path
        Absolute path to main file
        
    plot_list: list of strings
        A list containing the names of the plots to be plotted.
    
    """
    def __init__(self, info, abs_path, plot_list):

        (self.desired_animal_list,
         self.image_folder,
         self.proximity,
         self.animal_matrix,
         self.radius,
         self.animal,
         self.subject) = info

        self.plot_list = plot_list
        self.images_path = abs_path / self.image_folder / self.animal

        self.plots = self.__create_plot_objects(plot_list)
        self.final_data = []


    def __create_plot_objects(self, plot_list):
        '''
        create_plot_objects(plot_list)
        
        Creates a list that contains Plot objects based on the configuration ZipFile The class for reading and writing ZIP files.  See section 
        
        Parameters
        ----------
        plot_list : list of strings
            List containing the names of the plots required by configuration file
            
        Returns
        -------
        
        plots: list of Plot objects
            List containing the Plot objects created. 
            
        Example
        -------
        plot_list = ['static_trajectories','distance_bar']
        
        This list would return:
        plots = [StaticTrajectoriesPlot(), DistanceBarPlot()]
        
        
        
        '''
        plots = []

        if 'static_trajectories' in plot_list:
            s = StaticTrajectoriesPlot(self.desired_animal_list, isSaved=True)
            plots.append(s)
        if 'dynamic_trajectories' in plot_list:
            # l = LiveTrajectoriesPlot(
            #     self.desired_animal_list, isSaved=True, images_path=self.images_path)
            # plots.append(l)
            pass
        if 'distance_bar' in plot_list:
            b = DistanceBarPlot(self.desired_animal_list, isSaved=True)
            plots.append(b)
        if 'proximity_bar' in plot_list:
            pb = ProximityBarPlot(
                (self.desired_animal_list, self.proximity, self.radius), isSaved=True)
            plots.append(pb)
        if 'proximity_heatmap' in plot_list:
            phm = ProximityHeatmapPlot(
                (self.animal_matrix, self.radius), isSaved=True)
            plots.append(phm)
        if 'proximity_graph' in plot_list:
            pg = ProximityGraphPlot(
                (self.desired_animal_list, self.animal_matrix, self.radius), isSaved=True)
            plots.append(pg)
        if 'velocity_plot' in plot_list:
            vp = VelocityPlot((self.desired_animal_list), isSaved=True)
            plots.append(vp)
        if 'states' in plot_list:
            st = StatesPlot((self.desired_animal_list), isSaved=True)
            plots.append(st)
        if 'state_timeline' in plot_list:
            stt = StateTimelinePlot(
                (self.desired_animal_list, self.subject), isSaved=True)
            plots.append(stt)

        return plots

    def plot(self, plots):
        '''
        plot
        
        This method calls the prints the name of the plot and also plots the Plot.
        It destroys the Plots objects at the end (memory and performace).        
        '''
        
        
        # print('--------------------------------------')
        # print("You have selected the following plots:")
        # for plot in plots:
        #     print(plot)
        # print('--------------------------------------')
        for plot in self.plots:
            data = plot.plot()
            self.final_data.append(data)
            # print(data)
            # plot.destroy()
        return self.final_data

