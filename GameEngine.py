from typing import Union, Iterable


class Scene:

    def __init__(self, screen, *objects):
        self.screen = screen
        self.objects: Iterable[Object] = []

    def render(self):
        for obj in sorted(self.objects, key=lambda key: obj.z_sorting):
            obj.render()

    def tick(self, fps):
        for obj in self.objects:
            obj.tick()


class Object:

    def __init__(self, scene: Scene, z_sorting=0):
        self.scene = scene
        self.transform = Transform()
        self.parent = None
        self.z_sorting = z_sorting
        self.components = []

    def tick(self):
        for component in self.components:
            component.tick()

    def render(self):
        pass

    def add_component(self, component):
        self.components.append(component)

    def get_component(self, component):
        return self.components[self.components.index(component)]

    def delete_component(self, component):
        self.components.remove(component)

    def on_collision(self):
        pass


class Transform:

    def __init__(self):
        self.position = Vector2()
        self.rotation = Vector2()
        self.scale = Vector2()


class Component:

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name

    def tick(self, fps):
        pass


class Event:

    def __init__(self):
        self.subs = []

    def __call__(self, *args, **kwargs):
        for sub in self.subs:
            sub(*args, **kwargs)

    def __iadd__(self, other):
        self.subs.append(other)


class Vector2:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Input:

    codes_keys = {119: 'w', 97: 'a', 100: 'd', 115: 's', 113: 'q', 101: 'e', 114: 'r', 102: 'f', 122: 'z', 99: 'c',
                  118: 'v', 120: 'x', 116: 't', 103: 'g', 98: 'b', 27: 'esc', 49: '1', 50: '2', 51: '3', 52: '4',
                  53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 48: '0'}

    holding_keys = {"w": 0, "a": 0, "d": 0, "s": 0, "q": 0, "e": 0, "r": 0, "f": 0, "z": 0, "c": 0, "v": 0, "x": 0,
                    "t": 0, "g": 0, "b": 0, "esc": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0,
                    "8": 0,  "9": 0, "0": 0, "shift": 0, "tab": 0, "ctrl": 0}

    pressed_keys = {"w": 0, "a": 0, "d": 0, "s": 0, "q": 0, "e": 0, "r": 0, "f": 0, "z": 0, "c": 0, "v": 0, "x": 0,
                    "t": 0, "g": 0, "b": 0, "esc": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0,
                    "8": 0,  "9": 0, "0": 0, "shift": 0, "tab": 0, "ctrl": 0}

    released_keys = {"w": 0, "a": 0, "d": 0, "s": 0, "q": 0, "e": 0, "r": 0, "f": 0, "z": 0, "c": 0, "v": 0, "x": 0,
                     "t": 0, "g": 0, "b": 0, "esc": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0,
                     "8": 0,  "9": 0, "0": 0, "shift": 0, "tab": 0, "ctrl": 0}

    @staticmethod
    def get_key_down(key: str):
        if Input.pressed_keys[key]:
            return True
        else:
            return False

    @staticmethod
    def get_key(key: str):
        if Input.holding_keys[key]:
            return True
        else:
            return False

    @staticmethod
    def get_key_up(key: str):
        if Input.released_keys[key]:
            return True
        else:
            return False


def clamp(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]):
    """Return value limited by minimum and maximum value."""
    return max(min(value, max_value), min_value)
