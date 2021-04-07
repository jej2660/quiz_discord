import sqlite3


class Account:
    def __init__(self):
        self.db = sqlite3.connect("./acc.db",isolation_level=None)
        self.cur = self.db.cursor()
        self.updatequery = "UPDATE account SET value=? WHERE name=?"
        self.searchquery = "select * from account where name=?"
        self.addquery = "INSERT INTO account VALUES(?,?)"
        self.addstockquery = "INSERT INTO stock_market VALUES(?,0,0)"

    def update(self, name, value):
        self.cur.execute(self.updatequery, (value, name,))

    def search(self, name):
        self.cur.execute(self.searchquery, (name,))
        return self.cur.fetchall()

    def addUser(self, name):
        self.cur.execute(self.addquery, (name, 2000,))
        self.cur.execute(self.addstockquery,(name,))

    def updateMoney(self, name, value):
        data = self.search(name)
        datatu = data[0]
        deposit = datatu[1]
        deposit += value
        self.update(name, deposit)
    def currentDeposit(self, name):
        return "현재 잔액:" + str(self.search(str(name)))
    def currentDepositI(self, name):
        data = self.search(name)
        datatu = data[0]
        deposit = datatu[1]
        return int(deposit)
    
    def moneyRank(self):
        data = self.cur.execute("select * from account ORDER BY value DESC")
        return data.fetchall()
    
    def console(self, query):
        print(query)
        self.cur.execute(query)


if __name__ == "__main__":
    account = Account()
    data = account.moneyRank()
    print(data)
    for i in data:
        print(i)
    print(type(data))