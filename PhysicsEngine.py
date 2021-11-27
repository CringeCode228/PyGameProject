from math import pi


class RigidBody:
    pass


class Collider:

    def __init__(self, side, pos_x=0, pos_y=0, rot_x=0, rot_y=0):
        self.side = side
        self.position_x = pos_x
        self.position_y = pos_y
        self.rotation_x = rot_x
        self.rotation_y = rot_y


class CircleCollider(Collider):

    def __init__(self):
        super().__init__(pi)


class BoxCollider(Collider):

    def __init__(self):
        super().__init__(1)
