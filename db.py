import sqlite3

class Database:
    def __init__(self, dbName: str):
        self.__dbName = dbName
        self.__connection = sqlite3.connect(self.__dbName)
        self.__cursor = self.__connection.cursor()

    def addUserToDatabase(self, user_id: str, user_name: str):

        self.__cursor.execute(f"""INSERT INTO chat_members(user_id, user_name) 
                    VALUES('{user_id}', '{user_name}');""")
        self.__connection.commit()
        return "OK"

    def checkUserInDatabase(self, user_id: str):
        self.__cursor.execute(f"""SELECT user_id FROM chat_members WHERE user_id={user_id};""")
        result = self.__cursor.fetchone()
        if result is None:
            return False
        elif isinstance(result[0], str):
            return True

    def selectAll(self):
        self.__cursor.execute(f"""SELECT user_id, user_name FROM chat_members""")
        result = self.__cursor.fetchall()
        return result

