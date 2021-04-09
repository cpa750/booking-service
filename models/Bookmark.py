from util.Database import Database


class Bookmark:
    def __init__(self, db: Database, customer_id: str,
                 location_id: int = -1):
        self.__db = db
        self.customer_id = customer_id
        self.location_id = location_id
        self.__exists = False
        if location_id != -1:
            self.__get_from_database()
        if not self.__exists and location_id != -1:
            self.__write_to_db()

    def __get_from_database(self):
        rows = self.__db.read("SELECT * FROM Bookmark WHERE locationId = ? AND customerId = ?",
                              (self.location_id, self.customer_id))
        if len(rows) > 0:
            self.__exists = True
        else:
            self.__exists = False

    def __write_to_db(self):
        query_string = "INSERT INTO Bookmark (customerId, locationId) VALUES (?, ?)"
        self.__db.write(query_string,
                        (self.customer_id, self.location_id))
