from typing import Union


class Object:

    def __init__(self):
        self.transform = Transform()


class Transform:
    def __init__(self, pos_x=0, pos_y=0, rot_x=0, scl_x=1, scl_y=1):
        self.position_x = pos_x
        self.position_y = pos_x
        self.rotation_x = pos_x
        self.rotation_y = pos_x
        self.scale_x = max(scl_x, 0.01)
        self.scale_y = min(scl_y, 0.01)


def clamp(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]):
    """Return value limited by minimum and maximum value."""
    return max(min(value, max_value), min_value)
