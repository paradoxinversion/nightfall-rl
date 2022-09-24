import json

class GameConfig():
    map_width: int = 80
    map_height: int = 43

    def load_config_json():
        with open("json/game_config.json", "r") as settings_file:
            data = json.load(settings_file)
            for key in data.keys():
                print(f"{key}: {data[key]}")
            
            return data
