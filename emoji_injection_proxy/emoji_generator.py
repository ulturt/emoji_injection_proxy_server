import logging
import os
from typing import List, Optional, Generator

import emoji

logger = logging.getLogger(__name__)


DEFAULT_EMOJI_LIST = [
    ':smiling_imp:',
    ':sun_with_face:',
    ':octopus:',
    ':snake:',
    ':monkey:',
]


def extract_emojis_from_file() -> Optional[List[str]]:
    path_to_file = os.environ.get('EMOJI_LIST_FILE')
    if not (path_to_file and os.path.exists(path_to_file)):
        return
    try:
        with open(path_to_file) as file:
            # todo: validation
            return [line.strip() for line in file if line]
    except IOError:
        logger.error('Something went wrong during access to emoji list file.')


class EmojiGenerator:
    def __init__(self):
        self._emoji_list = extract_emojis_from_file() or DEFAULT_EMOJI_LIST
        self._emoji_generator = self._get_emoji()

    def generate(self) -> str:
        return next(self._emoji_generator)

    def _get_emoji(self) -> Generator[str, None, None]:
        i = 0
        while True:
            if i == len(self._emoji_list):
                i = 0
            yield emoji.emojize(self._emoji_list[i], use_aliases=True)
            i += 1


emoji_generator = EmojiGenerator()
