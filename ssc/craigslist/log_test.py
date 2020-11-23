import logging

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers for the custom logger
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('log_test.log', mode="w")
c_handler.setLevel(logging.NOTSET)
f_handler.setLevel(logging.NOTSET)

# Create formatters and add them to the handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

for x in range(10):
    logger.critical('This is a CRITICAL message.')
    logger.error('This is a ERROR message.')
    logger.warning('This is a WARNING message.')
    logger.info('This is a INFO message.')
    logger.debug('This is a DEBUG message.')

print(logger.getEffectiveLevel())