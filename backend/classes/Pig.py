from .Animal import Animal


class Pig(Animal):
    def __init__(self, id, x, y, bb_t, bb_l, bb_w, bb_h):
        super().__init__(id, x, y, bb_t, bb_l, bb_w, bb_h)

        self.type = "Pig"
        self.obtain_overall_state()
        self.concrete_states = self.obtain_concrete_states()

    def obtain_overall_state(self,
                                 very_active_threshold=25,
                                 passive_threshold=15,
                                 feeding_station=(200, 50)):
        '''TODO



        '''

        if self.avg_v > very_active_threshold:
            self.overall_state = "very_active"
            return
        if self.avg_v < passive_threshold:
            if self.near_feeding_station(self.avg_x, self.avg_y, (200, 125)):
                self.overall_state = "eating"
                return

            self.overall_state = "passive"
            return
        self.overall_state = "active"
        return

    def obtain_concrete_states(self, velocity_threshold=20):
        states = []
        for velocity, x, y, in zip(self.f_v, self.x, self.y):
            if velocity < velocity_threshold:
                if self.near_feeding_station(x, y):
                    states.append('eating')
                else:
                    states.append('sitting')
            else:
                states.append('moving')

        return states

    def near_feeding_station(self, x, y, feeding_station=(200, 125), eating_threshold=50):
        if (abs(x-feeding_station[0]) < eating_threshold
                and
                abs(y-feeding_station[1]) < eating_threshold):
            return True
        else:
            False
