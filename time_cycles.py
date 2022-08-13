class TimeCycle():
    def __init__(self, units_in_day, phase_transition_period):
        self._units_in_day = units_in_day
        self._tick_global = 0
        self._tick_day = 0

        self._phase_transition_period = phase_transition_period
        self._phase_in_transition = False
        self._remaining_phase_transition_ticks = 0

    @property
    def units_in_day(self):
        return self._units_in_day

    @property
    def tick_global(self):
        return self._tick_global

    @property
    def tick_day(self):
        return self._tick_day

    def tick(self):
        # Increment the daily and global tcik
        self._tick_day += 1
        self._tick_global += 1

        if self._phase_in_transition:
            self._remaining_phase_transition_ticks -= 1

        # Set day => night transitionary phase
        if self._tick_day == self.units_in_day / 2:
            # Set Transitionary Phase
            self.set_transition_phase(True)

        if self._tick_day > self._units_in_day:
            self._tick_day = 0


    def set_transition_phase(self, in_transition):
        self._phase_in_transition = in_transition
        if in_transition == True:
            self._remaining_phase_transition_ticks = self._phase_transition_period
    
    def return_phase(self):
        if self._tick_day <= self.units_in_day / 2:
            return "Day"
        return "Night"