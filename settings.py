import json


class Settings():
    def __init__(self, path):
        self.path = path
        self.map_path = None
        self.speed = None
        self.ghost_mode_time = None
        self.super_food_probability = None
        self.poisoned_food_probability = None

    def read_from_json(self):
        with open(self.path, 'r') as file_handle:
            data = json.load(file_handle)
            map_num = data['map_num']
            speed = data['speed']
            ghost_mode_time = data['ghost_mode_time']
            super_food_probability = data['super_food_probability']
            poisoned_food_probability = data['poisoned_food_probability']
        return (map_num, speed, ghost_mode_time, super_food_probability,
                poisoned_food_probability)

    def load(self):
        (map_num, speed, ghost_mode_time, super_food_probability,
         poisoned_food_probability) = self.read_from_json()
        self.map_path = f'maps/snake_map_{map_num}.txt'
        self.speed = (int(speed) * 60)
        self.ghost_mode_time = int(ghost_mode_time)
        self.super_food_probability = (int(super_food_probability) * 55) + 40
        self.poisoned_food_probability = ((int(poisoned_food_probability) * 55)
                                          + 40)

    def write_to_json(self, map_num, speed, ghost_mode_time,
                      super_food_probability, poisoned_food_probability):
        settings_data = {
            "map_num": map_num,
            "speed": speed,
            "ghost_mode_time": ghost_mode_time,
            "super_food_probability": super_food_probability,
            "poisoned_food_probability": poisoned_food_probability
        }
        with open(self.path, 'w') as file_handle:
            json.dump(settings_data, file_handle, indent=5)
