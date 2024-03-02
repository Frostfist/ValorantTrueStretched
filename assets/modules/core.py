import json
from dataclasses import dataclass
from re import match

PATH = "config/config.json"


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Config:
    def __init__(self) -> None:
        self.__update__()
        self.app_window = self.__get__("App")["Window"]
        self._resolutions = Resolutions()

    @property
    def fonts(self):
        return self.__get__("App")["Fonts"]

    @property
    def resolutions(self):
        return self._resolutions

    @property
    def search(self):
        return self.__get__("App")["Search"]

    @property
    def window(self):
        return Window(self)
    
    @property
    def title(self):
        return self.__get__("App")["Title"]

    def __set__(self, category, subcategory, key, value):
        self.data[category][subcategory][key] = value
        self.__save()
    def __get__(self, key: str) -> object:
        self.__update__()
        return self.data.get(key, None)
    def __save(self):
        with open(PATH, "w") as file:
            json.dump(self.data, file, indent=3)
    def __update__(self):
        with open(PATH, 'r') as file:
            self.data = json.load(file)

class Resolution(str):
    def __init__(self, x : int, y : int):
        self._resolution = (self.x, self.y)

    def __init__(self, resolution : tuple[int, int]):
        self._resolution = resolution

    def __init__(self, resolution : str):
        t = resolution.split("x")
        self._resolution = (t[0], t[1])
        
    def __str__(self) -> str:
        return self._resolution[0] + "x" + self._resolution[1]


@singleton
class Resolutions(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return super().__str__()

    def append(self, item : Resolution):
        if item not in self:
            super().append(item)

@singleton
class Window:
    def __init__(self, config):
        self._config : Config = config

    @property
    def width(self):
        return self._config.app_window["Width"]

    @width.setter
    def width(self, value):
        self._config.app_window["Width"] = value

    @property
    def height(self):
        return self._config.app_window["Height"]

    @height.setter
    def height(self, value):
        self._config.app_window["Height"] = value

    @property
    def max_width(self):
        return self._config.app_window["Max_Width"]

    @property
    def max_height(self):
        return self._config.app_window["Max_Height"]

    @property
    def resizable(self):
        return self._config.app_window["Resizable"]

    @property
    def min_width(self):
        return self._config.app_window["Min_Width"]

    @property
    def min_height(self):
        return self._config.app_window["Min_Height"]

@singleton
class Display:
    def __init__(self) -> None:
        pass

@singleton
class Valorant:
    def __init__(self) -> None:
        pass