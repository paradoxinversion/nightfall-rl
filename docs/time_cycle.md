# time_cycle

time_cycle is responsible for handling time in Nightfall. 

# TimeCycle class

The TimeCycle class is the class that brings time capability to Nightfall. The system works on ticks, each of which is a single 'unit' of time. A certain amount of ticks equals a day. Each action taken by players and npcs should require a certain amount of ticks before its execution is completed.

## TimeCycle Variables

unitsInDay
The total amount of units in a day. It should be divisible by two, as the first half of that amount is considered 'day' and the second half is considered 'night'.

tick_total
the current tick in the time cycle

tick_day
the current tick in the day

phase_transition_period
the amount of ticks it takes for day to become night and vice versa.

phase_in_transition
true if the phase is in transition from day to night, false otherwise.

TimeCycle Methods

tick
Move the clock forward a single unit. If the tick_day > unitsInDay, tick_day resets to 0.

set_transition_phase()