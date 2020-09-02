import logging
import bot_configuration
import heartbeat

#Adjust the logging based on mode
if bot_configuration.CONSOLE_LOGGING == True:
	logging.basicConfig(format=bot_configuration.LOG_FORMAT, level=bot_configuration.LOGGING_LEVEL)
else:
	logging.basicConfig(format=bot_configuration.LOG_FORMAT, filename=bot_configuration.DATA_FOLDER+bot_configuration.LOG_FILE,level=bot_configuration.LOGGING_LEVEL)

heartbeat.pulse()