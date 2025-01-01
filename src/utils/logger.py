import logging
import os

os.makedirs("log", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app_handler = logging.FileHandler("log/app.log")
app_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler("log/error.log")
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
app_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logger.addHandler(app_handler)
logger.addHandler(error_handler)
