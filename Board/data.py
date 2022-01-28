import json
import sqlite3
import hashlib
from main import Block, Player
from main import Level


class DataBase:

    @staticmethod
    def get_level_from_id(id):
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM Levels WHERE Levels.ID={id}")
        return cur.fetchall()

    @staticmethod
    def get_levels_from_name(name):
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM Levels WHERE Levels.name LIKE '%{id}%'")
        return cur.fetchall()

    @staticmethod
    def get_player(name, password):
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM Players WHERE Players.name AND password='{hashlib.sha256(password)}'")
        return cur.fetchall()

    @staticmethod
    def set_level(name, player_id, data):
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Levels (Name, Player, Data) VALUES ({name}, {player_id}, {data})")

    @staticmethod
    def set_player(name, password):
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Levels (Name, Password) VALUES ({name}, {password})")


class JSONUtility:

    IDS = {Block.get_id(): Block, Player.get_id(): Player}

    @staticmethod
    def serialize_level(level):
        data = []
        for object in level.objects:
            data.append(object.serialize())
        return "\n".join(data)

    @staticmethod
    def deserialize_level(data):
        level = Level()
        for i in data.split("\n"):
            level_object = json.loads(i)
            level.objects.append(JSONUtility.IDS[level_object["id"]](level_object))
        return level
