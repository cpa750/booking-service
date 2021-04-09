from util.Database import Database


class Customer:
    def __init__(self, db: Database, customer_id: str, name: str = "",
                 phone_no: str = ""):
        self.__db = db
        self.in_db = False
        self.customer_id = customer_id
        self.name = name
        self.phone_no = phone_no
        self.__get_from_db()

    def __get_from_db(self):
        rows = self.__db.read("SELECT * FROM Customer WHERE id = ?", (self.customer_id,))
        if len(rows) > 0:
            self.name = rows[0][1]
            self.phone_no = rows[0][2]
            self.in_db = True
        elif self.name != "" and self.phone_no != "":
            query_string = "INSERT INTO Customer (id, custName, phoneNo) VALUES (?, ?, ?)"
            self.__db.write(query_string, (self.customer_id, self.name, self.phone_no))

    def get_bookmarked_locations(self):
        query_string = "SELECT * FROM Bookmark WHERE customerId = ?"
        rows = self.__db.read(query_string, (self.customer_id,))
        if len(rows) > 0:
            return rows
        else:
            return False

    def get_no_of_reservations(self):
        query_string = "SELECT * FROM Reservation WHERE customerId = ?"
        rows = self.__db.read(query_string, (self.customer_id,))
        return len(rows)
