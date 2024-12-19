import re
import json as js
import dbfile as db
from translator import transenru

import time
import concurrent.futures


class Porter:
    PERFECTIVEGROUND = re.compile(
        u"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$")
    REFLEXIVE = re.compile(u"(с[яь])$")
    ADJECTIVE = re.compile(
        u"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$")
    PARTICIPLE = re.compile(u"((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$")
    VERB = re.compile(
        u"((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$")
    NOUN = re.compile(
        u"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$")
    RVRE = re.compile(u"^(.*?[аеиоуыэюя])(.*)$")
    DERIVATIONAL = re.compile(u".*[^аеиоуыэюя]+[аеиоуыэюя].*ость?$")
    DER = re.compile(u"ость?$")
    SUPERLATIVE = re.compile(u"(ейше|ейш)$")
    I = re.compile(u"и$")
    P = re.compile(u"ь$")
    NN = re.compile(u"нн$")

    def stem(word):
        try:
            word = word.lower()
            word = word.replace(u'ё', u'е')
            m = re.match(Porter.RVRE, word)
            if m.groups():
                pre = m.group(1)
                rv = m.group(2)
                temp = Porter.PERFECTIVEGROUND.sub('', rv, 1)
                if temp == rv:
                    rv = Porter.REFLEXIVE.sub('', rv, 1)
                    temp = Porter.ADJECTIVE.sub('', rv, 1)
                    if temp != rv:
                        rv = temp
                        rv = Porter.PARTICIPLE.sub('', rv, 1)
                    else:
                        temp = Porter.VERB.sub('', rv, 1)
                        if temp == rv:
                            rv = Porter.NOUN.sub('', rv, 1)
                        else:
                            rv = temp
                else:
                    rv = temp

                rv = Porter.I.sub('', rv, 1)

                if re.match(Porter.DERIVATIONAL, rv):
                    rv = Porter.DER.sub('', rv, 1)

                temp = Porter.P.sub('', rv, 1)
                if temp == rv:
                    rv = Porter.SUPERLATIVE.sub('', rv, 1)
                    rv = Porter.NN.sub(u'н', rv, 1)
                else:
                    rv = temp
                word = pre+rv
            return word
        except AttributeError:
            return
    stem = staticmethod(stem)


def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Заполнение базового случая
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Основной цикл
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Удаление
                dp[i][j - 1] + 1,      # Вставка
                dp[i - 1][j - 1] + cost  # Замена
            )

    return dp[m][n]


def similarity_percentage(str1, str2):
    # Расстояние Левенштейна
    distance = levenshtein_distance(str1, str2)
    # Длины строк
    max_length = max(len(str1), len(str2))
    if max_length == 0:  # Если обе строки пустые
        return 100.0
    # Процент схожести
    similarity = (1 - distance / max_length) * 100
    return round(similarity, 2)


def lexemes(file_name):
    lexemes = list()
    file_name = file_name.split('-')
    for word in file_name:
        lexemes.append('' + word)

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(Porter.stem, lexemes))
        results = [item for item in results if item is not None]

    return results


def induction(lexemes, channel_id):
    with open('data.json', 'r') as data:
        penis = js.load(data)
    for lexeme in lexemes:
        if not (lexeme in penis):
            penis[lexeme] = set()
        penis[lexeme] = set(penis[lexeme])
        penis[lexeme].add(channel_id)
        penis[lexeme] = list(penis[lexeme])

    with open('data.json', 'w') as data:
        js.dump(penis, data)


def search_link(lexems):
    with open('data.json', 'r') as data:
        penis = js.load(data)
    channels_list = list()
    keys = list(penis.keys())

    for lexem in lexems:
        for key in keys:
            if similarity_percentage(lexem, key) > 80:
                channels_list += penis[key]
    result = {}
    for channel in set(channels_list):
        result[channel] = channels_list.count(channel)

    result_id = sorted(result.items(), key=lambda item: item[1], reverse=True)
    result = []
    for id in [channel[0] for channel in (result_id[:5] if len(result_id) > 5 else result_id)]:
        result.append(db.ChanelService().get_by_id(id))
    return result
