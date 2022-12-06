# Time

Time is a central concept in Nightfall. The time of day determines what types of npc's and dangers the player might encounter. The level of danger a player can expect to face increases at night.

Each turn of the game is (currently) the shortest unit of time: a tick. A day in Nightfall is certain amount of ticks. There are two main phases of each day: daytime and nighttime. daytime occurs during each tick that is less than half of the total ticks in a day. nighttime occurs during each tick that is more than half that amount. The very first tick of each main phase (daytime/nighttime) triggers a transitionary phase. These transitionary phases can be considered dawn and dusk. During these transitionary phases, the base FoV range will respectively increase or decrease until day or night has fully set in.

As mentioned, each action currently takes one tick, whether it's using an item, attacking, waiting, moving, etc. Each action should take at least one tick, with more arduous ones (such as trying to force something open) taking more ticks than simple ones (taking a step).

Actions
Actions take one tick and represent what a character is doing moment to moment, such as moving or attacking.

Activities
Activities are actions that take multiple ticks, such as going somewhere, crafting something, etc.

NPCs and Time
At various times of the day, (most) NPCs will often go somewhere or do something. Before night time, citizens with homes will go home.

Evil NPCs
Evil NPCs have a cooldown time before their next atrocity. It is separated by day(s).

Related Docs
scripts/time_cycle.md