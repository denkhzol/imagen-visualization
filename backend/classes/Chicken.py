from .Animal import Animal


class Chicken(Animal):
    def __init__(self, id, x, y, bb_t, bb_l, bb_w, bb_h):
        super().__init__(id, x, y, bb_t, bb_l, bb_w, bb_h)
        self.type = "Chicken"
        self.obtain_overall_state()
        self.concrete_states = self.obtain_concrete_states()

    def obtain_overall_state(self,
                             very_active_threshold=40,
                             passive_threshold=10):
        '''TODO



        '''

        if self.avg_v > very_active_threshold:
            self.overall_state = "very_active"
            return
        if self.avg_v < passive_threshold:
            self.overall_state = "passive"
            return
        self.overall_state = "active"
        return

    def obtain_concrete_states(self, velocity_threshold=50):
        states = []
        for velocity, x, y, in zip(self.f_v, self.x, self.y):
            if velocity < velocity_threshold:
                states.append('sitting')
            else:
                states.append('moving')
        return states
