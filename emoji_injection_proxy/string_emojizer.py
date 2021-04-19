from emoji_injection_proxy.emoji_generator import emoji_generator as emoji

WORD_LENGTH = 6


def emojize_string(string: str) -> str:
    new_char_list = []
    counter = 0
    for char in string:
        char_is_alphabetic = char.isalpha()
        if char_is_alphabetic:
            counter += 1
        if counter and not char_is_alphabetic:
            if counter == WORD_LENGTH:
                new_char_list.append(emoji.generate())
            counter = 0
        new_char_list.append(char)
    return ''.join(new_char_list)
