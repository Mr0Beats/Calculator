import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] - %(levelname)s - %(module)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("MathApp")