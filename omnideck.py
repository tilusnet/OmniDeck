#!/usr/bin/env python3

import lib.config as config
import lib.omniglot as omniglot


def omnideck():
    langs = config.Language.active
    omniPhrases = omniglot.Phrases()
    for lang in langs:
        print(omniPhrases.get_lang_url(lang))


if __name__ == "__main__":
    omnideck()
