from load_map import Map
from load_map import (
    InvalidMapError, InvalidSnakeError, InvalidPathExtension
)
from pathlib import Path
import pytest


def test_map_init():
    map_path = Path(__file__).parent / "maps/snake_map_1.txt"
    map = Map(map_path)
    assert map.path == map_path
    assert map.walls == []
    assert map.snake_coords == [(29, 9)]


def test_map_init_walls():
    map_path = Path(__file__).parent / "test_maps/test_map_1.txt"
    map = Map(map_path)
    assert map.path == map_path
    assert map.walls == [(1, 1), (57, 1), (4, 9), (5, 9), (1, 17), (57, 17)]
    assert map.snake_coords == [(29, 9)]


def test_map_init_no_snake():
    with pytest.raises(InvalidSnakeError):
        map_path = Path(__file__).parent / "test_maps/test_map_2.txt"
        _ = Map(map_path)


def test_map_init_invalid_char():
    with pytest.raises(InvalidMapError):
        map_path = Path(__file__).parent / "test_maps/test_map_3.txt"
        _ = Map(map_path)


def test_map_init_missing_border():
    with pytest.raises(InvalidMapError):
        map_path = Path(__file__).parent / "test_maps/test_map_5.txt"
        _ = Map(map_path)


def test_map_init_invalid_path_extension():
    with pytest.raises(InvalidPathExtension):
        map_path = Path(__file__).parent / "test_maps/test_map_4.pdf"
        _ = Map(map_path)
