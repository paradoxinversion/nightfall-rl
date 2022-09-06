import json

class GameConfig():
    map_width: int = 80
    map_height: int = 43

    def load_config_json():
        f = open("json/game_config.json", "r")
        for x in f.readlines():
            print(x)
            # print(f"{f.readline()}")