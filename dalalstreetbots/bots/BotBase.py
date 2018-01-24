"""BotBase class"""

import asyncio

class BotBase(object):
    """BotBase class defines the base class for all bots"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    async def _hidden_init_(self, id, name, settings, bot_manager, indicator_manager, market_messenger):
        """_hidden_init is used by the Bot Manager. DO NOT OVERRIDE"""
        self.id = id
        self.name = name         # name is unique to each bot
        self.settings = {**self.default_settings, **settings} # override default settings with custom

        print(self.name, "init", self.settings, self.default_settings)

        self.__bot_manager = bot_manager # keep the bot_manager private
        self.__indicator_manager = indicator_manager # keep the indicator_manager private
        self.__market_messenger = market_messenger # keep the market messenger private
        self.__is_running = False # used to avoid running same bot multiple times simultaneously
        self.__should_run = False # used to pause/unpause the bot
        await self.load_indicators()

    async def load_indicators(self):
        """This must be overridden by subclasses if they need their own indicators"""
        pass

    async def get_my_cash(self):
        """get_my_cash returns the cash owned by the bot"""
        resp = await self.__market_messenger.get_portfolio(self.id)
        return resp.user.cash

    async def get_my_portfolio(self):
        """returns a map<int,int> key being the stockid and value being the number of owned stocks"""
        resp = await self.__market_messenger.get_portfolio(self.id)
        return resp.stocks_owned

    async def buy_stocks_from_exchange(self, stock_id, stock_quantity):
        """Buy stocks from Exchange"""
        return await self.__market_messenger.buy_stocks_from_exchange(
            self.id, stock_id, stock_quantity
        )

    async def place_buy_order(self, stock_id, stock_quantity, price):
        """place Bid order"""
        return await self.__market_messenger.place_buy_order(
            self.id, stock_id, stock_quantity, price
        )

    async def place_sell_order(self, stock_id, stock_quantity, price):
        """place ask order"""
        return await self.__market_messenger.place_sell_order(
            self.id, stock_id, stock_quantity, price
        )

    async def cancel_order(self, order_id, is_ask):
        """cancel buy/sell order"""
        return await self.__market_messenger.cancel_order(
            self.id, order_id, is_ask
        )

    async def run(self):
        """Run the bot. DO NOT OVERRIDE. Should be called only once!"""
        if self.__is_running:
            return

        self.__is_running = True
        self.__should_run = True
        while self.__should_run:
            await asyncio.sleep(self.settings["sleep_duration"])
            await self.update()

    def pause(self):
        """Pauses the bot's execution. DO NOT OVERRIDE."""
        self.__should_run = False

    async def update(self):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        pass

    async def get_indicator(self, indicator_type, stock_id, indicator_settings):
        """returns an indicator"""
        return await self.__indicator_manager.get_indicator(indicator_type, stock_id, indicator_settings)
