from GameEngine import *
from math import pi

g = 9.81


class OnCollision(Event):

    def __init__(self):
        super(OnCollision, self).__init__()


class RigidBody(Component):

    def __init__(self, obj):
        super(RigidBody, self).__init__(obj, "RigidBody")
        self.velocity = Velocity()

    def on_collison(self,):

    def tick(self, fps):
        self.velocity.line_velocity.y -= g / fps
        self.obj.transform.position.x += self.velocity.line_velocity.x / fps
        self.obj.transform.position.y += self.velocity.line_velocity.y / fps
        self.obj.transform.rotation.x += self.velocity.angular_velocity.x / fps
        self.obj.transform.rotation.y += self.velocity.angular_velocity.y / fps


class Velocity:

    def __init__(self):
        self.line_velocity = Vector2()
        self.angular_velocity = Vector2()


class Collider(Component):

    def __init__(self, obj):
        super(Collider, self).__init__(obj, "Collider")

    def calculate(self, scene):
        pass


class CircleCollider(Collider):

    def __init__(self, obj):
        super().__init__(obj)


class BoxCollider(Collider):

    def __init__(self, obj):
        super().__init__(obj)

    def calculate(self, scene):
        for obj in scene.objects:
            for component in obj.components:
                if type(component) == BoxCollider:
                    # TODO: calculate collision with box collider
                    collision = False
                    if collision:
                        self.obj.on_collision()
                        obj.on_collision()
                    pass
