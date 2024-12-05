from abc import ABC
from .auxiliary import calculate_2d_distance
from numpy import sqrt, average


class Animal(ABC):
    '''
    Animal
    
    This is the abstract class of Animal. It contains the basic attributes and
    methods of the animals. It is extended to Chicken and Pig.
    
    Parameters
    ----------
    id : int   
        integer identifying the animal
    x,y: double
        x,y positions of the animal in the frame. These are the center of the
        bounding box, calculated as:
        x = bb_left + bb_width / 2
        y = bb_top + bb_height / 2
    bb_t, bb_l: double
        bb_t(bb_l) is the coordinate of the top(left) corner of the bounding box
    bb_w, bb_h: double
        these are the width and the height of the bounding box.

    
    '''
    def __init__(self, id, x, y, bb_t, bb_l, bb_w, bb_h):
        self.id = id

        self.x = x
        self.y = y

        self.bb_t = bb_t
        self.bb_l = bb_l
        self.bb_w = bb_w
        self.bb_h = bb_h

        self.avg_x = average(self.x)
        self.avg_y = average(self.y)
        self.avg_w = average(self.bb_w)
        self.avg_h = average(self.bb_h)

        self.calculate_distance()
        self.calculate_speed()
        self.calculate_areas()

        self.frame_count = len(self.x)
        self.type = "Animal"

    def calculate_distance(self):
        '''
        calculate_distance()
        
        Calculates the distance traveled of the animal.

        On each step it meassures Euclidean distance between 
        x[i],y[i] and x[i+1],y[i+1] and adds it to a counter 
        variable (distance).


        '''
        x_old, y_old = self.x[0], self.y[0]
        distance = 0
        for x, y in zip(self.x[1:], self.y[1:]):
            distance += calculate_2d_distance(x,
                                              x_old,
                                              y,
                                              y_old)
            x_old = x
            y_old = y
        self.distance = distance

    def calculate_speed(self, video_duration=60, fps=30):
        """
        calculate_speed(video_duration, fps)
        
        Calculates the x and y components of the velocity on the 
        animal. Also the velocity modulus.

        It takes the positions x and y and obtains the velocity by 
        substracting two continuous positions and dividing by the 
        time difference. The average speed is calculated with numpy. 
        f_vx and f_vy are equal velocity vector but have
        one extra element so the velocity vector is equal 
        in size to the positions vector.

        """
        x = self.x
        y = self.y

        seconds_per_frame = video_duration / fps

        vx = [(y - x)/seconds_per_frame for x, y in zip(x, x[1:])]
        vy = [(y - x)/seconds_per_frame for x, y in zip(y, y[1:])]


        f_vx = vx.copy()
        f_vx.append(vx[-1])
        f_vy = vy.copy()
        f_vy.append(vy[-1])

        self.vx = vx
        self.vy = vy
        self.f_vx = f_vx
        self.f_vy = f_vy

        # lets calculate the total modulus speed
        v = [sqrt(vx*vx+vy*vy) for vx, vy in zip(vx, vy)]
        self.v = v

        f_v = [sqrt(vx*vx+vy*vy) for vx, vy in zip(f_vx, f_vy)]
        self.f_v = f_v

        self.avg_v = average(v)

    def calculate_areas(self):
        """
        calculate_areas()
        
        calculate the areas of the bounding box:
        area = widht * height
        
        """
        self.areas = [w*h for w, h in zip(self.bb_h, self.bb_w)]

    def append_position(self, posx, posy):
        '''
        append_position(posx, posy)
        
        Appends posx,posy to the list of positions x,y
        
        '''
        self.x.append(posx)
        self.y.append(posy)

    def set_position(self, x, y):
        '''
        set_position(x, y)
        
        Sets the position x,y    
                
        '''
        self.x = x
        self.y = y

    def get_distance(self):
        '''
        get_distance()
        
        Returns the distance 
                
        '''
        return self.distance

    def get_x(self):
        '''
        get_x()
        
        Returns x
                
        '''
        return self.x

    def get_y(self):
        '''
        get_y()
        
        Returns y
                
        '''
        return self.y
