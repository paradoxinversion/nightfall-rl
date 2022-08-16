engine.py is the director of sorts of the game.

Engine
The engine class 

Class Vars
game_map: GameMap
game_world: GameWorld
time_cycle: TimeCycle

Instance Vars
message_log
mouse_location
player
A reference to the player

time_cycle
A reference to the time_cycle instance.

current_fov_radius
The player's current modified FoV radius. This needs to be captured outside of the update_fov function

Methods

saveAs(self, filename: str)
Saves the instance of the engine as a compressed file.

handle_enemy_turns
Iterates through all entities. If they have AI, performs the action associated with their current AI mode.