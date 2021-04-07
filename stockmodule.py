import requests
from money import *

class Stock:
    def __init__(self, acc):
        self.acc = acc
        self.ETHstockquery = "UPDATE stock_market SET ETH=? WHERE name=?"
        self.BTCstockquery = "UPDATE stock_market SET BTC=? WHERE name=?"
        self.searchstock = "SELECT * FROM stock_market WHERE name=?"
        self.btc_url = "https://api.bithumb.com/public/orderbook/BTC_KRW"
        self.eth_url = "https://api.bithumb.com/public/orderbook/ETH_KRW"
        self.market = {"BTC":999999999999, "ETH":999999999999}
        self.activemarket = ["BTC", "ETH"]
    def getBTCinfo(self):
        res = requests.get(self.btc_url)
        res = res.json()
        self.market["BTC"] = int(res['data']['asks'][0]['price'])
        return self.market["BTC"]
    def getETHinfo(self):
        res = requests.get(self.eth_url)
        res = res.json()
        self.market["ETH"] = int(res['data']['asks'][0]['price'])
        return self.market["ETH"]

    def getOwnStock(self, name):
        data = self.acc.cur.execute("select * from stock_market where name=?", (name,))
        if data == []:
            return -1
        data = data.fetchone()
        return {"BTC":data[1], "ETH": data[2]}
    def updateStock(self, name, market, value):
        ownstock = self.getOwnStock(name)
        choicedmarket = ownstock[market] + value
        if market == 'BTC':
            self.acc.cur.execute(self.BTCstockquery, (choicedmarket, name))
        elif market == 'ETH':
            self.acc.cur.execute(self.ETHstockquery, (choicedmarket, name))

    def buystock(self, name, market, cnt):
        self.getBTCinfo()
        self.getETHinfo()
        cnt = float(cnt)
        if self.market[market] * cnt > self.acc.currentDepositI(name):
            return 1
        self.acc.updateMoney(name, -self.market[market] * cnt)
        #data = self.acc.cur.execute("SELECT ETH FROM stock_market where name='Sgom#5840'")
        old = self.acc.cur.execute(self.searchstock, (name,))
        old = old.fetchone()
        choice = 2 if market == "ETH" else 1
        if choice == 1:
            total = old[choice] + cnt
            self.acc.cur.execute(self.BTCstockquery, (total,name))
        elif choice == 2:
            total = old[choice] + cnt
            self.acc.cur.execute(self.ETHstockquery, (total,name))
        return 0

    def sellStock(self, name, market, cnt):
        data = self.getOwnStock(name)
        if data[market] < cnt:
            return -1
        
        totalMoney = self.market[market] * cnt
        self.acc.updateMoney(name, totalMoney)
        self.updateStock(name,market, -cnt)

    


        

if __name__ == '__main__':
    stock = Stock(Account())
    print(stock.getOwnStock("Sgom#5840"))
    stock.updateStock("Sgom#5840","BTC", 1)
    #stock.sellStock("Sgom#5840","ETH",1)
    #print(stock.getOwnStock("Sgom#5840"))
    #print(stock.acc.currentDeposit("Sgom#5840"))
    #stock.buystock("Sgom#5840", "ETH", "0.0001")
