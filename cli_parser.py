import argparse
import logging
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


class CommandLineParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Отправка сообщения между пользователями.")
        self.parser.add_argument("sender", help="Номер отправителя")
        self.parser.add_argument("recipient", help="Номер получателя")
        self.parser.add_argument("message", help="Текст сообщения")
        self.args = self.parser.parse_args()
        logger.info(f"readed data from CLI {self.args}")

    def get_sender(self) -> str:
        """Возвращает номер отправителя."""
        return self.args.sender

    def get_recipient(self) -> str:
        """Возвращает номер получателя."""
        return self.args.recipient

    def get_message(self) -> str:
        """Возвращает текст сообщения."""
        return self.args.message
