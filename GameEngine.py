from typing import Union


class Scene:

    def __init__(self, *objects):
        self.objects = []

    def render(self):
        for obj in sorted(self.objects, key=lambda key: obj.z_sorting):
            obj.render()


class Object:

    def __init__(self, z_sorting=0):
        self.transform = Transform()
        self.parent = None
        self.z_sorting = z_sorting
        self.components = []

    def render(self, screen):
        pass

    def add_component(self, component):
        self.components.append(component)

    def get_component(self, component):
        return self.components[self.components.index(component)]

    def delete_component(self, component):
        self.components.remove(component)


class Transform:

    def __init__(self, pos_x=0, pos_y=0, rot_x=0, rot_y=0, scl_x=1, scl_y=1):
        self.position_x = pos_x
        self.position_y = pos_y
        self.rotation_x = rot_x
        self.rotation_y = rot_y
        self.scale_x = scl_x
        self.scale_y = scl_y


class Component:

    def __init__(self):
        pass


def clamp(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]):
    """Return value limited by minimum and maximum value."""
    return max(min(value, max_value), min_value)
