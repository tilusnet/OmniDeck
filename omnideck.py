#!/usr/bin/env python3

import requests
import pycountry
import lib.config as config
import lib.omniglot as omniglot
from bs4 import BeautifulSoup as bsoup
from bs4 import Tag as bsoupTag

import json



def commit_parsed_entry(parsed_list, entry):
    entry['text'] = entry['text'].strip()
    parsed_list.append(entry)

def concatenate_tag_contents(tag):
    result = ''
    for child in tag.children:
        if isinstance(child, bsoupTag):
            if child.name == 'br':
                result += '<br/>'
            elif child.name == 'em':
                result += '<i>' + child.string + '</i>'
        elif isinstance(child, str):
            result += child
    return result


def parse_block(block, combined_result=False, links=True):
    parsed = []

    beginning = True
    parsed_entry = {'text': '', 'link': ''}
    for entry in block:
        if isinstance(entry, bsoupTag):
            if entry.name == 'a':
                if not beginning and not combined_result:
                    # </a> tags are parsed entry boundaries:
                    # 'commit' parsed entry
                    commit_parsed_entry(parsed, parsed_entry)
                    parsed_entry = {'text': '', 'link': ''}
                parsed_entry['text'] += concatenate_tag_contents(entry)
                if links:
                    # store the link -- to what we expect to be the sound file
                    parsed_entry['link'] = entry['href']
            elif entry.name == 'br':
                # <br/> tags mark a new line
                parsed_entry['text'] += '<br/>'
            elif entry.name == 'em':
                parsed_entry['text'] += '<i>' + concatenate_tag_contents(entry) + '</i>'
        elif isinstance(entry, str):
            # string instances get added to the current parsed entry
            parsed_entry['text'] += entry
        beginning = False
    # finally commit the last parsed entry as well
    commit_parsed_entry(parsed, parsed_entry)
    # and return it
    return parsed



def omnideck():
    langs = config.Language.active
    omniPhrases = omniglot.Phrases()
    results = []
    for lang in langs:
        language_name = pycountry.languages.get(iso639_1_code=lang).name
        url = omniPhrases.get_lang_url(lang)
        webpage_data = requests.get(url).text
        data_table = bsoup(webpage_data).select('body div#bodybox div#body div#unicode table')[0]
        for entry in data_table.select('> tr')[1:]:
            english_block, targetlang_block = [ e.contents for e in entry.find_all(name='td', limit=2, recursive=False) ]
            english = parse_block(english_block, combined_result=True, links=False)
            targetlang = parse_block(targetlang_block)
            results.append({
                'English'        : english,
                'TargetLang'     : targetlang,
                'TargetLangName' : language_name
            })
    print(json.dumps(results[:10], indent=2, ensure_ascii=False))




if __name__ == "__main__":
    omnideck()
