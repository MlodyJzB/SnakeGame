from settings import Settings
from pathlib import Path


def test_settings_init():
    settings_path = Path(__file__).parent / "settings.json"
    settings = Settings(settings_path)
    assert settings.path == settings_path
    assert settings.map_path is None
    assert settings.speed is None
    assert settings.ghost_mode_time is None
    assert settings.super_food_probability is None
    assert settings.super_food_probability is None


def test_settings_read_from_json():
    path = "test_settings/test_settings_1.json"
    settings_path = Path(__file__).parent / path
    settings = Settings(settings_path)
    (map_num, speed, ghost_mode_time, super_food_probability,
     poisoned_food_probability) = settings.read_from_json()
    assert map_num == '2'
    assert speed == '8'
    assert ghost_mode_time == '10'
    assert super_food_probability == '4'
    assert poisoned_food_probability == '2'


def test_settings_load():
    path = "test_settings/test_settings_1.json"
    settings_path = Path(__file__).parent / path
    settings = Settings(settings_path)
    settings.load()
    assert settings.path == settings_path
    assert settings.map_path == 'maps/snake_map_2.txt'
    assert settings.speed == 480
    assert settings.ghost_mode_time == 10
    assert settings.super_food_probability == 260
    assert settings.poisoned_food_probability == 150


def test_settings_load_2():
    path = "test_settings/test_settings_2.json"
    settings_path = Path(__file__).parent / path
    settings = Settings(settings_path)
    settings.load()
    assert settings.path == settings_path
    assert settings.map_path == 'maps/snake_map_custom.txt'
    assert settings.speed == 60
    assert settings.ghost_mode_time == 1
    assert settings.super_food_probability == 590
    assert settings.poisoned_food_probability == 95


def test_settings_write_to_json():
    path = "test_settings/test_settings_3.json"
    settings_path = Path(__file__).parent / path
    settings = Settings(settings_path)

    settings.write_to_json('custom', '1', '1', '10', '1')
    settings.load()

    assert settings.path == settings_path
    assert settings.map_path == 'maps/snake_map_custom.txt'
    assert settings.speed == 60
    assert settings.ghost_mode_time == 1
    assert settings.super_food_probability == 590
    assert settings.poisoned_food_probability == 95

    settings.write_to_json('6', '2', '2', '2', '2')
    settings.load()

    assert settings.path == settings_path
    assert settings.map_path == 'maps/snake_map_6.txt'
    assert settings.speed == 120
    assert settings.ghost_mode_time == 2
    assert settings.super_food_probability == 150
    assert settings.poisoned_food_probability == 150

    settings.write_to_json('custom', '1', '1', '10', '1')
    settings.load()

    assert settings.path == settings_path
    assert settings.map_path == 'maps/snake_map_custom.txt'
    assert settings.speed == 60
    assert settings.ghost_mode_time == 1
    assert settings.super_food_probability == 590
    assert settings.poisoned_food_probability == 95
