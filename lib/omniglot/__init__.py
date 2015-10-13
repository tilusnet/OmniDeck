#!/usr/bin/env python3

import pycountry

hostname = 'http://omniglot.com'


class Phrases:
    
    _base_url = hostname + '/language/phrases'
    _url_by_lang_template = _base_url + '/{lang}.php'
    _url_by_phrase_template = _base_url + '/{phrase}.htm'

    def get_lang_url(self, lang_id):
        language = pycountry.languages.get(iso639_1_code=lang_id)
        return self._url_by_lang_template.format(lang=language.name.lower())

    def get_phrase_url(self, phrase_id):
        return self._url_by_phrase_template.format(phrase=phrase_id)
