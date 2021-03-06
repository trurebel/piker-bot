import state_db
import brokerage
import logging
import trades_manager
import trades_db
import time
import requests
import trade_journal
import bot_configuration
import stock_math

s = state_db.StateDB(bot_configuration.DATA_FOLDER + bot_configuration.DATABASE_NAME)
b = brokerage.Brokerage(bot_configuration.ALPACA_PAPER_TRADING_ON, bot_configuration.ALPACA_KEY_ID, bot_configuration.ALPACA_SECRET_KEY, bot_configuration.DATA_FOLDER)
j = trade_journal.TradeJournal(bot_configuration.TRADE_JOURNAL_TITLE)
db = trades_db.DB(j, bot_configuration.DATA_FOLDER + bot_configuration.DATABASE_NAME)
sm = stock_math.StockMath()

def pulse():
	try:
		trades_manager.pull_queued_trades(db, j)
		
		is_open = b.is_open()
		#is_open = True

		logging.info(f'Heartbeat Pulse {time.time()}: Market Open - {is_open}')

		if (is_open == None):
			logging.error('Brokerage API failed to return market status.')
			return
		elif is_open == False:
			if s.get_market_open() == True:
				logging.critical('Market has closed.')
				s.set_market_open(False)
			return

		if s.get_market_open() == False:
			s.set_market_open(True)
			logging.critical('Market has opened')

		trades_manager.expire_trades(b, db)
		trades_manager.handle_open_buy_orders(b, db, s)
		trades_manager.handle_open_sell_orders(b, db, s)
		trades_manager.handle_open_trades(b, db, s, sm)
		trades_manager.open_new_trades(b, db, s, sm)


	except requests.exceptions.ConnectionError as conn:
		logging.error(f'Bad connection. {str(conn)}')

	except Exception as err:
		logging.error('Exception occured during heartbeat:', exc_info=err)
