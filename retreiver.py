#!/bin/env python


from transliterate import translit
import hunspell
import requests
from bs4 import BeautifulSoup
import urllib.parse
gpt_key = "sk-proj-SWNqwtvt6luWjiP586uAT3BlbkFJTlAn6Y2MIal8mDO5yIG1"

cons = ['б', 'в', 'х', 'г', 'д', 'ж', 'з', 'п', 'ф', 'к', 'т', 'ш', 'с', ]
suffixes = ['а', 'аемый', 'аж', 'ак', 'аль', 'альный',
            'ан', 'ание', 'анин', 'анка', 'анный',
            'аной', 'ануть', 'аный', 'анье', 'арь',
            'астый', 'ат', 'атор', 'атый', 'ать',
            'ация', 'ач', 'ающий', 'ающийся', 'ба',
            'бес', 'бесие', 'бина', 'бище', 'вать',
            'го', 'дей', 'е', 'ебный', 'ев',
            'еватый', 'евать', 'евик', 'евина',
            'евич', 'евня', 'евой', 'евский',
            'евый', 'ед', 'ее', 'ей', 'ек', 'ель',
            'енец', 'ение', 'енный', 'еный',
            'енье', 'енька', 'енький', 'енько', 'ески',
            'еский', 'ество', 'ествовать',
            'еть', 'ец', 'ечка', 'ечко', 'ёв', 'ёвый',
            'ёж', 'ёк', 'ёнка', 'ёнок', 'ёный',
            'ёр', 'жды', 'знь', 'ивать', 'ивый', 'ие',
            'изировать', 'изм', 'изна', 'ий',
            'ийски', 'ийский', 'ик', 'ика', 'илище',
            'ильный', 'имый', 'ин', 'ина', 'инец',
            'инский', 'инство', 'иный', 'иня', 'ировать',
            'ист', 'истый', 'ит', 'ить', 'ифицировать',
            'иха', 'ица', 'ич', 'ический', 'ичка', 'ичный',
            'ишка', 'ище', 'ия', 'ійскій', 'ка',
            'кать', 'кий', 'ко', 'кун', 'ла', 'либо',
            'ливый', 'лище', 'лка', 'ло', 'лог',
            'логия', 'лый', 'ль', 'льник', 'льня', 'льщик',
            'лявый', 'надцать', 'нибудь', 'ний',
            'ник', 'ница', 'ничать', 'ной', 'ность', 'нуть',
            'ный', 'ня', 'няк', 'о', 'ов', 'оватый',
            'овать', 'овик', 'овина', 'ович', 'овка', 'овна',
            'овня', 'овой', 'овский', 'овской',
            'овый', 'ой', 'ок', 'он', 'онка', 'онный', 'онок',
            'онька', 'онький', 'ость', 'ота',
            'отня', 'очка', 'с', 'сан', 'ск', 'ски', 'ский',
            'ской', 'стан', 'ство', 'ствовать',
            'сь', 'ся', 'таки', 'тель', 'тельный', 'тельский',
            'тельство', 'ти', 'тие', 'ть', 'тян',
            'у', 'уля', 'ун', 'уть', 'уха', 'учий', 'ушка', 'ушки']

w_select_prompt = "You are a helpful linguist. Match the given word with the best construction-related jargon from the list. Return only the fitting word."

deff_prompt = "You are a dictionary entry picker. Pick the best Romanian deffiniton that fits the construction context (eg. materials, instruments). And display only your choice. If the definition is not present, return NONE."

tr_prompt = "You are a technical translation software similar to google translate. You specialize in instruments and construction materials. Translsate from Russian to Romanian. Give only the Rommanian translation."

# img_prompt = "You are an image picker. You return the "


def make_list_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    lines = text.split('\n')
    result = []
    current_element = []

    for line in lines:
        if line.strip() == '':
            if current_element:
                result.append(' '.join(current_element))
                current_element = []
        else:
            current_element.append(line)

    if current_element:
        result.append(' '.join(current_element))

    return result


def rm_suffix(word):
    for suffix in suffixes:
        if word.endswith(suffix):
            print("no suf: ", word[:-len(suffix)])
            return word[:-len(suffix)]
    return None


def hun_ru(text):
    hobj = hunspell.HunSpell('ru_RU.dic', 'ru_RU.aff')

    tr = translit(text, 'ru')
    if hobj.spell(tr):
        return [tr]
    elif len(hobj.suggest(tr)) == 0:
        return None
    return hobj.suggest(tr)


def hun_ro(tr):
    hobj = hunspell.HunSpell('ro_RO.dic', 'ro_RO.aff')
    if hobj.spell(tr):
        return [tr]
    elif len(hobj.suggest(tr)) == 0:
        return None
    return hobj.suggest(tr)


def yandex_retreiver(text):
    tr = translit(text, 'ru')
    url = 'https://speller.yandex.net/services/spellservice.json/checkText'
    res = requests.get(url, params={'text': tr})
    obj = res.json()
    if obj == []:
        return [tr]
    li = obj[0]['s']
    return li


def process_variations(tr):
    variations = [
        lambda s: s.replace('и', 'ы'),
        lambda s: s.replace('ц', 'к'),
        lambda s: s.replace('а', 'о'),
        lambda s: s.replace('с', 'ш')
    ]

    res = []

    # Apply each variation to the input string tr
    for variation in variations:
        for v2 in variations:
            res.append(variation(tr))

    return res


def russificator(text):
    tr = translit(text, 'ru')
    # res = process_variations(tr)
    res = []
    res.append(tr.replace('а', 'о'))
    res.append(tr.replace('иа', 'я'))
    res.append(tr)
    if tr[-1] in cons:
        new = tr + 'ь'
        res.append(new)
    # w_suf = rm_suffix(text)
    # if w_suf is not None:
    #    res.append(w_suf)

    print("translits:", res)
    return res


def rus_retreiver(words):
    res = []
    for text in words:
        ya = yandex_retreiver(text)
        hu = hun_ru(text)
        for w in hu + ya:
            res.append(w)
    return res


def get_first_word(txt):
    words = txt.split()
    return words[0]


def translate(word):
    url = "https://translate.googleapis.com/translate_a/t?anno=1&client=te&v=1.0&format=html&sl=ru&tl=ro&tk=322131.134890"
    res = requests.post(url, data={'q': word})
    print(res)
    exit()
    return


def str_for_req(input_string):
    formatted_string = input_string.replace('\n', '\\n')
    formatted_string = formatted_string.replace(
        '\\', '\\\\').replace('"', '\\"')
    url_encoded_string = urllib.parse.quote(formatted_string)
    return url_encoded_string


def chat(s, p):
    url = "https://api.openai.com/v1/chat/completions"
    messages = [
        {"role": "system", "content": s},
        {"role": "user", "content": str_for_req(p)}
    ]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt_key}"
    }
    data = {
        "model": "gpt-4o",
        "messages": messages
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 200:
        obj = resp.json()
        return obj['choices'][0]['message']['content']
    print(resp)
    return None


def dex(t):
    url = f"https://dexonline.ro/definitie/{t.strip()}/definitii"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    span_tags = soup.find_all('span', class_='def')
    res = ""
    for span in span_tags:
        res += span.text + '\\n'
    return res


def retreiver(text):
    ro = hun_ro(text)
    print(ro)
    ro_selected = ""
    ro_res = ""
    if ro is not None and len(ro) > 0:
        if len(ro) == 1:
            ro_selected = ro[0]
        else:
            ro_selected = chat(w_select_prompt, f"'{text}': {ro}")
    defs = dex(ro_selected)
    if defs is not None:
        ro_res = chat(deff_prompt, defs)

    ru = rus_retreiver(russificator(text))
    ru_selected = ""
    ru_res = ""
    if ru is not None and len(ru) > 0:
        if len(ru) == 1:
            ru_selected = ru[0]
        else:
            p = f"'{text}': {ru}"
            print(p)
            ru_selected = chat(w_select_prompt, p)
            print("sel: ", ru_selected)
            tr = chat(tr_prompt, ru_selected)
            print("tr: ", tr)
            deffs = dex(tr)
            if deffs is None:
                deffs = dex(get_first_word(tr))
        ru_res = chat(deff_prompt, deffs)
    return {"ro": [ro_selected, ro_res],
            "ru": [ru_selected + ' - ' + tr, ru_res]}


# q = input()
##
# print(retreiver(q))
