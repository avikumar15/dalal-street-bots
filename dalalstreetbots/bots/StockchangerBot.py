from bots.BotBase import BotBase
import math

class StockchangerBot(BotBase):
    """A mindless bot to increase or decrease price based on what we want to do.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, # number of companies to buy at a time
        "stocks_per_company":1, # how many stocks per company do you want to buy at a time
        "holding_time": 5, # how many rounds to hold before you sell your stocks off
        "no_of_companies": 1, # number of companies to buy from
        "bot_tag": "unset", # special tags for searching purpose
        "impact": 0,
        "stockId":0,
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [company_id, ema , latest_price]

    async def load_indicators(self):
        self.stockchangerindicator = {}
        for i in range(1, self.settings["no_of_companies"]+1):
            self.stockchangerindicator[i] = await self.get_indicator("StockchangerIndicator", i, {
                "type": "prices",
            })

    async def update(self, *args, **kwargs):
        correct_indicator = self.stockchangerindicator[self.settings['stockId']]
        stock_price = correct_indicator.price
        if (stock_price != 0):
            stock_price = math.floor(stock_price + stock_price*self.settings['impact'])
            if self.settings['impact'] > 0:
                await self.place_buy_order(self.settings['stockId'], self.settings['stocks_per_company'], stock_price, 0)
            if self.settings['impact'] < 0:
                await self.place_sell_order(self.settings['stockId'], self.settings['stocks_per_company'], stock_price, 0)
            print(self.name + " just ran now")