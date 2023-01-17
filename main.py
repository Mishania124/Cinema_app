import sqlite3


class Seat:

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def check_availability(self):
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
        cursor.execute("""
                SELECT "availability" FROM "cinema" WHERE "seat_id"=?
                """, [self.seat_id])
        res = cursor.fetchone()[0]
        connection.close()
        return res

    def buy_seat(self):
        connection = sqlite3.connect('cinema.db')
        connection.execute("""
        UPDATE "cinema" SET "availability"=? WHERE "seat_id"=?
        """, [1 if self.check_availability() == 0 else 1, self.seat_id])
        connection.commit()
        connection.close()

    def get_prise(self):
        connection = sqlite3.connect('cinema.db')
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT "price" FROM "cinema" WHERE "seat_id"=?
                        """, [self.seat_id])
        res = cursor.fetchone()[0]
        connection.close()
        return res


class Card:

    def __init__(self, type, number, user, cvc, money=2000):
        self.cvc = cvc
        self.type = type
        self.number = number
        self.user = user
        self.money = money

    def add_user(self):
        connection = sqlite3.connect('banking.db')
        connection.execute("""
        INSERT INTO "banking" ("type","numer","cvc","fullname","count") VALUES (?, ?, ?,?,?)
        """, [self.type, self.number, self.cvc, self.user, self.money])
        connection.commit()
        connection.close()

    def get_count(self):
        connection = sqlite3.connect('banking.db')
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT "count" FROM "banking" WHERE "numer"=?
                        """, [self.number])
        res = cursor.fetchone()[0]
        connection.close()
        return res

    def buy_tick(self):
        connection = sqlite3.connect('banking.db')
        connection.execute("""
            UPDATE "banking" SET "count"=? WHERE "numer"=? AND "cvc"=?
            """, [self.get_count() - Seat(st).get_prise(), self.number, self.cvc])
        connection.commit()
        connection.close()

    def get_n_card(self):
        connection = sqlite3.connect('banking.db')
        cursor = connection.cursor()
        cursor.execute("""
                                SELECT "numer" FROM "banking" WHERE "fullname"=?
                                """, [self.user])
        res = cursor.fetchone()[0]
        connection.close()
        return res

    def get_cvc_card(self):
        connection = sqlite3.connect('banking.db')
        cursor = connection.cursor()
        cursor.execute("""
                                SELECT "cvc" FROM "banking" WHERE "fullname"=?
                                """, [self.user])
        res = cursor.fetchone()[0]
        connection.close()
        return res

    def get_t_card(self):
        connection = sqlite3.connect('banking.db')
        cursor = connection.cursor()
        cursor.execute("""
                                SELECT "type" FROM "banking" WHERE "fullname"=?
                                """, [self.user])
        res = cursor.fetchone()[0]
        connection.close()
        return res


name = str(input('Enter your full name: '))
st = str(input('Enter your seat: '))
s = Seat(st)
while s.check_availability() != 0:
    st = str(input('Ticket is not available! Try to buy another seat: '))
    s = Seat(st)
t_card = str(input('Enter your type of Card: '))
n_card = int(input('Enter your Card numer: '))
cvc_card = int(input('Enter your CVC: '))

c = Card(t_card, n_card, name, cvc_card)

if t_card == c.get_t_card() and n_card == c.get_n_card() and cvc_card == c.get_cvc_card():
    c.buy_tick()
    s.buy_seat()
    print(f'Mr./Mrs. {name} bought a ticket number {st}!')
else:
    print('Problems with your card identification! Try again!')
