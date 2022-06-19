import datetime
from random import randint

from constants import GREEK_ALPHABET


class NamingUtil:
    @staticmethod
    def random_name() -> str:
        return GREEK_ALPHABET[randint(0, len(GREEK_ALPHABET))]

    @staticmethod
    def now() -> datetime:
        return datetime.datetime.now().replace(microsecond=0)

    @staticmethod
    def format_iso(date):
        return date.isoformat().replace(":", "")
