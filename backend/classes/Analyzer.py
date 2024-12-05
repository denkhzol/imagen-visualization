import numpy as np
import sys
from .Pig import Pig
from .Chicken import Chicken
from .Plotter import Plotter
from .auxiliary import calculate_2d_distance

class Analyzer(object):
    '''TODO'''

    def __init__(self, reader, configuration):
        self.rd = reader            # Reader object
        self.df = self.rd.get_df()  # Obtains the dataframe
        self.conf = configuration   # Obtains the configuration
        self.abs_path = reader.abs_path

        self.animal_dict = {"pig": Pig,
                            "chicken": Chicken}

        self.__configure()          # Applies the configuration

        self.__analyze()            # Starts the analysis
        self.data = []

    def __configure(self):
        '''TODO'''
        # Folder
        self.image_folder = self.abs_path / \
            self.conf.configuration['image_folder']



        # Type of animal
        self.animal = self.conf.configuration['animal']
        self.subject = self.conf.configuration['subject']

        try:
            if self.animal not in ["pig", "chicken"]:
                raise NameError('Unknown animal.')
        except NameError:
            print("ERROR: The animal '{}' is not accepted. Try 'pig' or 'chicken'.".format(
                self.animal))
            raise
            sys.exit()

        self.animal_list = self.__populate_animals(self.animal)
        self.desired_animal_indices = self.conf.configuration['desired_animal_indices']

        if "all" in self.desired_animal_indices:
            self.desired_animal_list = self.animal_list
        else:
            self.desired_animal_list = [
                animal for animal in self.animal_list if animal.id[0] in self.desired_animal_indices]

        # Some variables
        self.radius = self.conf.configuration['radius']
        if self.radius == 0:
            # print("-------------------------------------")
            # print("You introduced 0 as searching radius.")
            # print("Suggesting radius...")
            self.radius = self.suggest_radius()
        self.frame_count = self.__count_frames()
        self.animal_count = self.__count_animals()
        self.desired_count = len(self.desired_animal_list)
        
        passive, very_active = self.suggest_thresholds()
        # print(passive, very_active)
        
        for animal in self.desired_animal_list:
            animal.obtain_overall_state(very_active, passive)

        self.proximity = self.__meassure_proximity(radius=self.radius,
                                                   list1=self.desired_animal_list,
                                                   list2=self.desired_animal_list)

        # if all(v == 0 for v in self.proximity):
        #     print("-------------------------------------------------------------")
        #     print("WARNING: proximity list is empty. Probably radius is too small.")
        #     print("-------------------------------------------------------------")
        #     print("")

        self.animal_matrix = self.__create_proximity_matrix(self.radius)

        # Packs information for plotter
        self.info = (self.desired_animal_list,
                     self.image_folder,
                     self.proximity,
                     self.animal_matrix,
                     self.radius,
                     self.animal,
                     self.subject)

    def __count_animals(self):
        return self.df['Id'].nunique()

    def __count_frames(self):
        return self.df['Frame'].nunique()

    def __analyze(self):
        plot_list = self.conf.configuration['desired_plots']
        try:
            if plot_list is None:
                raise ValueError
        except ValueError:
            print(
                "----------------------------------------------------------------------")
            print(
                "ERROR: Please select at least one plot type in the configuration file.")
            print(
                "----------------------------------------------------------------------")
            sys.exit()

        # Prints some information in the screen
        self.__print_information()

        # Creates the plotter object
        pt = Plotter(self.info, self.abs_path, plot_list)

        data = pt.plot(plot_list)
        return data
        
        

    def __print_information(self):
        # print('')
        # print('--------------------------------------')
        # print("Your data contains:" + "{}".format(self.animal).rjust(19, ' '))
        # print("Number of animals in the scene:" +
        #       "{}".format(self.animal_count).rjust(7, ' '))
        # print("Number of frames:" + "{}".format(self.frame_count).rjust(21, ' '))
        # print('--------------------------------------')
        # print('')
        pass

    def __populate_animals(self, animal):
        animal_list = []
        for key, grp in self.df.groupby(['Id']):

            x = grp['x'].to_numpy()
            y = grp['y'].to_numpy()
            bb_l = grp['bb_left'].to_numpy()
            bb_t = grp['bb_top'].to_numpy()
            bb_w = grp['bb_width'].to_numpy()
            bb_h = grp['bb_height'].to_numpy()
            animal_list.append(self.animal_dict[animal](
                key, x, y, bb_l, bb_t, bb_w, bb_h))

        return animal_list

    def __meassure_proximity(self, radius, list1, list2):

        proximity = [0] * self.desired_count
        for frame in range(self.frame_count):
            i = 0
            for animal1 in list1:
                for animal2 in list2:
                    if animal1.id == animal2.id:
                        continue
                    else:
                        dist = calculate_2d_distance(animal1.x[frame],
                                                     animal2.x[frame],
                                                     animal1.y[frame],
                                                     animal2.y[frame])

                        if dist < radius:
                            proximity[i] += 1
                i += 1

        return proximity

    def __create_proximity_matrix(self, radius):

        animal_matrix = np.zeros((self.animal_count, self.animal_count))
        for frame in range(self.frame_count):
            i = 0
            for animal1 in self.animal_list:
                j = 0
                for animal2 in self.animal_list:
                    if animal1.id == animal2.id:
                        pass
                    else:
                        dist = calculate_2d_distance(animal1.x[frame],
                                                     animal2.x[frame],
                                                     animal1.y[frame],
                                                     animal2.y[frame])

                        if dist < radius:
                            animal_matrix[i, j] += 1

                    j += 1

                i += 1

        return animal_matrix

    def suggest_radius(self):

        average_width_list = []
        average_height_list = []

        animals = self.desired_animal_list

        for animal in animals:
            average_width_list.append(animal.avg_w)
            average_height_list.append(animal.avg_h)
            
            
        def geo_mean(iterable):
            a = np.array(iterable)
            return a.prod()**(1.0/len(a))

        average_width = int(np.average(average_width_list))
        average_height = int(np.average(average_height_list))
        
        # average_width = int(geo_mean(average_width_list))
        # average_height = int(geo_mean(average_height_list))

        print("The average width of an animal in these scenes is: {} pixels.".format(
            average_width))
        print("The average height of an animal in these scenes is: {} pixels.".format(
            average_height))
        # radius = np.average([average_height, average_width])

        radius = geo_mean([average_height, average_width])
        radius = int(radius)
        print("Suggested radius is: {}".format(radius))
        return radius


    def suggest_thresholds(self):
        animals = self.desired_animal_list
        
        average_velocities = []
        velocities = []
        
        for animal in animals:
            average_velocities.append(animal.avg_v)
            velocities.append(animal.v)
            
        mean = np.mean(average_velocities)
        std = np.std(average_velocities)
        
        
        def normal_dist(x , mean , sd):
            prob_density = (1/(np.sqrt(2*np.pi)*sd)) * np.exp(-0.5*((x-mean)/sd)**2)
            return prob_density
        
        x1 = np.min(average_velocities)
        x2 = np.max(average_velocities)
        
        x = np.linspace(x1, x2, 50)
        pdf = normal_dist(x,mean,std)
        
        
        
        a = 1
        passive_threshold = mean-a*std
        very_active_threshold = mean+a*std
        return passive_threshold, very_active_threshold
        
        
        flat_velocities = [item for sublist in velocities for item in sublist]
        mean = np.mean(flat_velocities)
        std = np.std(flat_velocities)
        
        pdf2 = normal_dist(flat_velocities, mean, std)
        
