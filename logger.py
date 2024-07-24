import logging

def conf_logger():
	logger = logging.getLogger(__name__)

	logger.setLevel(logging.DEBUG)

	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG)

	fh = logging.FileHandler("app.log")
	fh.setLevel(logging.INFO)

	formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s")
	fh.setFormatter(formatter)

	logger.addHandler(sh)
	logger.addHandler(fh)

	return logger

logger = conf_logger()