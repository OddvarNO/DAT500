# coding: utf-8
# Code for selectolax copied from: https://rushter.com/blog/python-fast-html-parser/
# Code for removing stopwords: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
# Code for extracting links: https://www.tutorialspoint.com/python_text_processing/python_extract_url_from_text.htm
from time import time
import warc
from selectolax.parser import HTMLParser
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy
import json

# NSFW
PROFANE_WORDS = {'omorashi', 'blowjob', 'scat', 'snowballing', 'shitty', 'tits', 'tribadism', 'strap on', 'hot carl', 'wank', 'twat', 'zoophilia', 'spic', 'homoerotic', 'pisspig', 'jailbait', 'bastardo', 'shemale', 'xx', 'butthole', 'yaoi', 'kinkster', 'bastard', 'faggot', 'shit', 'frotting', 'beaner', 'baby juice', 'poontang', 'sultry women', 'female squirting', 'nigga', 'strapon', 's&m', 'gay sex', 'nudity', 'darkie', 'vibrator', 'genitals', 'male squirting', 'birdlock', 'date rape', 'double penetration', 'sucks', 'tub girl', 'rapist', 'urophilia', 'fisting', 'blumpkin', 'piece of shit', 'poop chute', 'nigger', 'poon', 'doggiestyle', 'rimjob', 'splooge', 'bullshit', 'ponyplay', 'yiffy', 'dvda', 'alabama hot pocket', 'beaver lips', 'double dong', 'donkey punch', 'slanteye', 'eat my ass', 'babeland', 'wetback', 'spread legs', 'bondage', 'nambla', 'feltch', 'masturbate', 'juggs', 'kinbaku', 'twinkie', 'bollocks', 'fucking', 'pedobear', 'beaners', 'dendrophilia', 'erotism', 'pussy', 'barenaked', 'queaf', 'porn', 'twink', 'knobbing', 'neonazi', 'raping', 'shitblimp', 'coon', 'blonde action', 'reverse cowgirl', 'spooge', 'girl on', 'acrotomophilia', 'porno', 'creampie', 'piss pig', 'doggie style', 'futanari', 'femdom', 'hentai', 'towelhead', 'god damn', 'topless', 'bangbros', 'sodomy', 'nig nog', 'bulldyke', 'black cock', 'clusterfuck', 'bukkake', 'felch', 'jigaboo', 'white power', 'boob', 'guro', 'rectum', 'doggy style', 'kinky', 'sexy', 'coprolagnia', 'undressing', 'muffdiving', 'blow job', 'dolcett', 'blonde on blonde action', 'shibari', 'punany', 'ass', 'tushy', 'anal', 'hooker', 'humping', 'dildo', 'wrinkled starfish', 'ball gag', 'gang bang', 'g-spot', 'pleasure chest', 'dry hump', 'camgirl', 'brown showers', 'anilingus', 'sodomize', 'bestiality', 'coons', 'carpetmuncher', 'schlong', 'auto erotic', 'lemon party', 'goatcx', 'intercourse', 'hand job', '2g1c', 'nude', 'domination', 'boner', 'boobs', 'make me come', 'kike', 'group sex', 'bimbos', 'how to kill', 'jail bait', 'fellatio', 'circlejerk', 'menage a trois', 'style doggy', 'queef', 'goodpoop', 'pissing', 'alaskan pipeline', 'panty', 'girls gone wild', 'tainted love', 'rosy palm and her 5 sisters', 'muff diver', 'autoerotic', 'goregasm', 'jack off', 'orgasm', 'dingleberry', 'bung hole', 'handjob', 'dirty sanchez', 'quim', 'mound of venus', 'pole smoker', 'rosy palm', 'big tits', 'big knockers', 'shrimping', 'threesome', 'poopchute', 'grope', 'strip club', 'two girls one cup', 'honkey', 'motherfucker', 'tongue in a', 'strappado', 'asshole', 'cornhole', 'goatse', 'jerk off', 'blue waffle', 'violet wand', 'deep throat', 'butt', 'dog style', 'camslut', 'dick', 'deepthroat', 'barely legal', 'fucktards', 'fuckin', 'dp action', 'arsehole', 'wrapping men', 'dominatrix', 'santorum', 'swastika', 'tight white', 'big breasts', 'jiggerboo', 'anus', 'upskirt', 'cunnilingus', 'titty', 'buttcheeks', 'doggystyle', 'bareback', 'playboy', 'nipple', 'camwhore', 'mr hands', 'big black', 'fingering', 'how to murder', 'brunette action', 'milf', 'cock', 'sadism', 'foot fetish', 'giant cock', 'phone sex', 'huge fat', 'penis', 'vagina', 'ejaculation', 'voyeur', 'shaved beaver', 'shota', 'pedophile', 'camel toe', 'jiggaboo', 'dommes', 'carpet muncher', 'busty', 'rimming', 'paedophile', 'suicide girls', 'orgy', 'nsfw images', 'escort', 'booty call', 'rape', 'bastinado', 'cunt', 'nipples', 'tied up', 'scissoring', 'titties', 'taste my', 'sex', 'spunk', 'cum', 'semen', 'baby batter', 'prince albert piercing', 'one cup two girls', 'urethra play', 'ecchi', 'fingerbang', 'missionary position', 'tubgirl', 'vorarephilia', 'jizz', 'nimphomania', 'wet dream', 'xxx', 'nympho', 'ball kicking', 'erotic', 'tit', 'golden shower', 'goo girl', 'blow your load', 'one guy one jar', 'ball sucking', 'assmunch', 'incest', 'pornography', 'coprophilia', 'lolita', 'poof', 'nymphomania', 'eunuch', 'cocks', 'fudge packer', 'pegging', 'pthc', 'hardcore', 'paki', 'jelly donut', 'tosser', 'panties', 'shaved pussy', 'bdsm', 'sexo', 'gokkun', 'venus mound', 'chocolate rosebuds', 'footjob', 'pubes', 'bitches', 'beaver cleaver', 'clitoris', '2 girls 1 cup', 'hard core', 'swinger', 'skeet', 'clover clamps', 'dirty pillows', 'ball licking', 'raging boner', 'ball sack', 'leather restraint', 'hot chick', 'throating', 'rusty trombone', 'splooge moose', 'bullet vibe', 'bunghole', 'fecal', 'suck', 'leather straight jacket', 'octopussy', 'vulva', 'tranny', 'slut', 'fuck buttons', 'snatch', 'girl on top', 'negro', 'dingleberries', 'bbw', 'cumming', 'tea bagging', 'ball gravy', 'nawashi', 'cleveland steamer', 'daterape', 'apeshit', 'lovemaking', 'raghead', 'fudgepacker', 'yellow showers', 'clit', 'smut', 'fuck', 'figging', 'bitch'}
ENGLISH_STOPWORDS = set(stopwords.words('english'))

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def get_text_selectolax(html):
    tree = HTMLParser(html)
    if tree.body is None:
        return None

    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator='')
    return text


def read_doc(record):
    url = record.url
    data = {}
    profanities = 0

    if url:
        if record.type == 'response':
            line = str(url)
            data["url"] = line[:line[11:].find("/")+11]
        payload = record.payload.read()
        header, html = payload.split(b'\r\n\r\n', maxsplit=1)

        # Header:
        if len(header) > 0: 
            header = get_text_selectolax(header)
            if record.type == "metadata":
                if header.find('"code":"') != -1:
                    return header[header.find('"code":"') + 8 : header.find('"code":"')+10]

            if header.find('Server: ') != -1:
                start_index = header.find('Server: ') + len('Server: ')
                end_index = start_index + header[start_index:].find("\n")   # if the start_index is not -1
                data["server"] = header[start_index:end_index]

        # HTML:
        # Must get links from unparsed text, to get all links from a site.
        html = html.strip()
        if len(html) > 0:
            parsed_text = get_text_selectolax(html)
            if parsed_text != None:
                # Links in the header are not considered since there where so few when it was checked.
                data["neighbor_urls"] = set(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(html)))
                parsed_text = re.sub(r'\n', ' ', parsed_text).strip()
                # parsed_text = re.sub(r"[^A-Za-z0–9]", " ", parsed_text).lower() # Removing all special characters (OBS: Dette vil fjerne alle ikke latinske bokstaver)
                # tokens = word_tokenize(parsed_text) # String to tokens
                # parsed_text = [word for word in tokens if not word in ENGLISH_STOPWORDS] # Removing stopwords
                # parsed_text_list = []
                # for word in tokens:
                #     if not word in ENGLISH_STOPWORDS:
                #         parsed_text_list.append(word)
                #     if word in PROFANE_WORDS:
                #         profanities += 1
                # parsed_text = " ".join(tokens) # Tokens to string
                data["parsed_text"] = parsed_text.strip('\n')
                data["profanities"] = profanities
    return data

def process_warc(file_name, limit=10000):
    warc_file = warc.open(file_name, 'rb')
    t0 = time()
    records = []
    n_documents = 0
    record_data = {}
    for i, record in enumerate(warc_file):
        if record['WARC-Type'] == "request":
            record_data = {}
        elif record['WARC-Type'] == "response":
            record_data = read_doc(record)
            continue
        elif record['WARC-Type'] == "metadata":
            record_data['language'] = read_doc(record)
            pass
        if not bool(record_data): # checking if dict is empty
            continue
        records.append(record_data)

        n_documents += 1

        if n_documents % 1000 == 0:
            print("Processed {} documents.".format(n_documents))

        if i > limit:
            break

    warc_file.close()
    print('Parsing took %s seconds and produced %s documents\n' % (time() - t0, n_documents))
    return records


if __name__ == '__main__':

    data = process_warc('/home/ubuntu/cc-mrjob/crawl-data/CC-MAIN-2022-05/segments/1642320299852.23/warc/CC-MAIN-20220116093137-20220116123137-00000.warc.gz', limit = 100)


    with open("processed_data.json", "w", encoding="utf8") as json_file:
        json.dump(data, json_file, cls=SetEncoder)

