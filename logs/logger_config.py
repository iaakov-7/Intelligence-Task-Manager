import logging

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s",
                    level=logging.INFO,
                    handlers=[logging.FileHandler("logs/app.log"),
                              logging.StreamHandler()])

logger = logging.getLogger()