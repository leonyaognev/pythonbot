import re
import json as js
import dbfile as db
from translator import transenru


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
    stem = staticmethod(stem)


def lexemes(file_name):
    lexemes = list()
    file_name = file_name.split()
    for word in file_name:
        word = transenru(word)
        try:
            lexemes.append(Porter.stem(u'' + word))
        except:
            continue
    return lexemes


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
    for lexem in lexems:
        if lexem in penis:
            channels_list += penis[lexem]
    result = {}
    for channel in set(channels_list):
        result[channel] = channels_list.count(channel)

    result_id = sorted(result.items(), key=lambda item: item[1], reverse=True)
    result = []
    for id in [channel[0] for channel in (result_id[:5] if len(result_id) > 5 else result_id)]:
        result.append(db.ChanelService().get_link_by_id(id))
    return result
