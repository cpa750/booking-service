from util.Database import Database


class Location:
    def __init__(self, db: Database, location_id: int = None, name: str = "",
                 address: str = "", email: str = ""):
        self.__db = db
        self.location_id = location_id
        self.name = name
        self.address = address
        self.email = email
        self.exists = False
        if location_id is not None:
            self.__get_from_db()
        if not self.exists:
            self.__write_to_db()

    def __get_from_db(self):
        rows = self.__db.read("SELECT * FROM Location WHERE id = ?", (self.location_id,))
        if len(rows) > 0:
            self.name = rows[0][1]
            self.address = rows[0][2]
            self.email = rows[0][3]
            self.exists = True

    def __write_to_db(self):
        query_string = "INSERT INTO Location (name, address, email) VALUES (?, ?, ?)"
        self.__db.write(query_string, (self.name, self.address, self.email))
