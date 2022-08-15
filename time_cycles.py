class TimeCycle():
    def __init__(self, phase_ticks_dawn, phase_ticks_daytime, phase_ticks_dusk, phase_ticks_nighttime):
        # How many total ticks have occured in the game?
        self._tick_global = 0

        # How many ticks have occured in this day?
        self._tick_day = 0

        self._current_phase = 0 # phases: 0 - dawn, 1 - day, 2 - dusk, 3 - night
        self._phases = {
            "dawn": phase_ticks_dawn,
            "daytime": phase_ticks_daytime,
            "dusk": phase_ticks_dusk,
            "nighttime": phase_ticks_nighttime
        }
        self._remaining_phase_ticks = 0
    @property
    def current_phase_name(self) -> str:
        """Returns the key of _phases (after running _phases.keys())"""
        return list(self._phases.keys())[self._current_phase]

    @property
    def units_in_day(self) -> int:
        ticks_in_day = 0
        for phase_ticks in self._phases.values():
            ticks_in_day += phase_ticks
        return ticks_in_day

    @property
    def tick_global(self):
        return self._tick_global

    @property
    def tick_day(self):
        return self._tick_day

    def debug(self):
        print(f"Debug Time Cycles")
        print(self.current_phase_name)
        for key in self.__dict__.keys():
            print(f"{key}: {self.__dict__.get(key)}")
        
    def set_remaining_phase_ticks(self, phase):
        """Set _remaing_phase_ticks to the total amount of ticks in a given phase"""
        if self._phases.get(phase) is not None:
            self._remaining_phase_ticks = self._phases.get(phase)
        else:
            print(f"Unable to set phase transition ticks, phase {phase} does not exist")
            pass
        

    def tick(self):
        self.debug()
        # Increment the daily and global tick amt
        self._tick_day += 1
        if self._tick_day > self.units_in_day:
            self._tick_day = 0

        self._tick_global += 1
        
        # get a list of the remaining phase ticks

        # if we're on the first tick of the day (0), it's dawn
        if self._tick_day == 0:
            self._current_phase = 0
            self.set_remaining_phase_ticks("dawn") 
        if self._tick_day == self._phases.get("dawn"):
            self._current_phase = 1
            self.set_remaining_phase_ticks("daytime")
        if (self._tick_day == (self._phases.get("dawn") + self._phases.get("daytime"))):
            self._current_phase = 2
            self.set_remaining_phase_ticks("dusk")
        if (self._tick_day == (self._phases.get("dawn") + self._phases.get("daytime") + self._phases.get("dusk"))):
            self._current_phase = 3
            self.set_remaining_phase_ticks("nighttime")
    
    def return_phase(self):
        # mapping of phase names to display names
        phase_map = {
            "dawn": "Dawn",
            "daytime": "Day",
            "dusk": "Evening",
            "nighttime": "Night"
        }
        return phase_map[self.current_phase_name]