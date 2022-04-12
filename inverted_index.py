
from mrjob.job import MRJob
import re
# import sys
# from profanity_filter import ProfanityFilter
# import spacy


class MRInvertedIndex(MRJob):
    
    # INPUT_PROTOCOL = JSONProtocol
    # sys.stderr.write(str(sys.path))
    def mapper(self, _, record):
        # Copied from: https://github.com/chucknorris-io/swear-words/blob/master/en
        # profanities = {'omorashi', 'blowjob', 'scat', 'snowballing', 'shitty', 'tits', 'tribadism', 'strap on', 'hot carl', 'wank', 'twat', 'zoophilia', 'spic', 'homoerotic', 'pisspig', 'jailbait', 'bastardo', 'shemale', 'xx', 'butthole', 'yaoi', 'kinkster', 'bastard', 'faggot', 'shit', 'frotting', 'beaner', 'baby juice', 'poontang', 'sultry women', 'female squirting', 'nigga', 'strapon', 's&m', 'gay sex', 'nudity', 'darkie', 'vibrator', 'genitals', 'male squirting', 'birdlock', 'date rape', 'double penetration', 'sucks', 'tub girl', 'rapist', 'urophilia', 'fisting', 'blumpkin', 'piece of shit', 'poop chute', 'nigger', 'poon', 'doggiestyle', 'rimjob', 'splooge', 'bullshit', 'ponyplay', 'yiffy', 'dvda', 'alabama hot pocket', 'beaver lips', 'double dong', 'donkey punch', 'slanteye', 'eat my ass', 'babeland', 'wetback', 'spread legs', 'bondage', 'nambla', 'feltch', 'masturbate', 'juggs', 'kinbaku', 'twinkie', 'bollocks', 'fucking', 'pedobear', 'beaners', 'dendrophilia', 'erotism', 'pussy', 'barenaked', 'queaf', 'porn', 'twink', 'knobbing', 'neonazi', 'raping', 'shitblimp', 'coon', 'blonde action', 'reverse cowgirl', 'spooge', 'girl on', 'acrotomophilia', 'porno', 'creampie', 'piss pig', 'doggie style', 'futanari', 'femdom', 'hentai', 'towelhead', 'god damn', 'topless', 'bangbros', 'sodomy', 'nig nog', 'bulldyke', 'black cock', 'clusterfuck', 'bukkake', 'felch', 'jigaboo', 'white power', 'boob', 'guro', 'rectum', 'doggy style', 'kinky', 'sexy', 'coprolagnia', 'undressing', 'muffdiving', 'blow job', 'dolcett', 'blonde on blonde action', 'shibari', 'punany', 'ass', 'tushy', 'anal', 'hooker', 'humping', 'dildo', 'wrinkled starfish', 'ball gag', 'gang bang', 'g-spot', 'pleasure chest', 'dry hump', 'camgirl', 'brown showers', 'anilingus', 'sodomize', 'bestiality', 'coons', 'carpetmuncher', 'schlong', 'auto erotic', 'lemon party', 'goatcx', 'intercourse', 'hand job', '2g1c', 'nude', 'domination', 'boner', 'boobs', 'make me come', 'kike', 'group sex', 'bimbos', 'how to kill', 'jail bait', 'fellatio', 'circlejerk', 'menage a trois', 'style doggy', 'queef', 'goodpoop', 'pissing', 'alaskan pipeline', 'panty', 'girls gone wild', 'tainted love', 'rosy palm and her 5 sisters', 'muff diver', 'autoerotic', 'goregasm', 'jack off', 'orgasm', 'dingleberry', 'bung hole', 'handjob', 'dirty sanchez', 'quim', 'mound of venus', 'pole smoker', 'rosy palm', 'big tits', 'big knockers', 'shrimping', 'threesome', 'poopchute', 'grope', 'strip club', 'two girls one cup', 'honkey', 'motherfucker', 'tongue in a', 'strappado', 'asshole', 'cornhole', 'goatse', 'jerk off', 'blue waffle', 'violet wand', 'deep throat', 'butt', 'dog style', 'camslut', 'dick', 'deepthroat', 'barely legal', 'fucktards', 'fuckin', 'dp action', 'arsehole', 'wrapping men', 'dominatrix', 'santorum', 'swastika', 'tight white', 'big breasts', 'jiggerboo', 'anus', 'upskirt', 'cunnilingus', 'titty', 'buttcheeks', 'doggystyle', 'bareback', 'playboy', 'nipple', 'camwhore', 'mr hands', 'big black', 'fingering', 'how to murder', 'brunette action', 'milf', 'cock', 'sadism', 'foot fetish', 'giant cock', 'phone sex', 'huge fat', 'penis', 'vagina', 'ejaculation', 'voyeur', 'shaved beaver', 'shota', 'pedophile', 'camel toe', 'jiggaboo', 'dommes', 'carpet muncher', 'busty', 'rimming', 'paedophile', 'suicide girls', 'orgy', 'nsfw images', 'escort', 'booty call', 'rape', 'bastinado', 'cunt', 'nipples', 'tied up', 'scissoring', 'titties', 'taste my', 'sex', 'spunk', 'cum', 'semen', 'baby batter', 'prince albert piercing', 'one cup two girls', 'urethra play', 'ecchi', 'fingerbang', 'missionary position', 'tubgirl', 'vorarephilia', 'jizz', 'nimphomania', 'wet dream', 'xxx', 'nympho', 'ball kicking', 'erotic', 'tit', 'golden shower', 'goo girl', 'blow your load', 'one guy one jar', 'ball sucking', 'assmunch', 'incest', 'pornography', 'coprophilia', 'lolita', 'poof', 'nymphomania', 'eunuch', 'cocks', 'fudge packer', 'pegging', 'pthc', 'hardcore', 'paki', 'jelly donut', 'tosser', 'panties', 'shaved pussy', 'bdsm', 'sexo', 'gokkun', 'venus mound', 'chocolate rosebuds', 'footjob', 'pubes', 'bitches', 'beaver cleaver', 'clitoris', '2 girls 1 cup', 'hard core', 'swinger', 'skeet', 'clover clamps', 'dirty pillows', 'ball licking', 'raging boner', 'ball sack', 'leather restraint', 'hot chick', 'throating', 'rusty trombone', 'splooge moose', 'bullet vibe', 'bunghole', 'fecal', 'suck', 'leather straight jacket', 'octopussy', 'vulva', 'tranny', 'slut', 'fuck buttons', 'snatch', 'girl on top', 'negro', 'dingleberries', 'bbw', 'cumming', 'tea bagging', 'ball gravy', 'nawashi', 'cleveland steamer', 'daterape', 'apeshit', 'lovemaking', 'raghead', 'fudgepacker', 'yellow showers', 'clit', 'smut', 'fuck', 'figging', 'bitch'}
        # nlp = spacy.load('en')
        # profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
        # pf = ProfanityFilter()
        # nlp.add_pipe(profanity_filter.spacy_component, last=True)
        if record.find("'Language': 'en'") != -1:
            splits = record.lower().split(",")
            server = splits[0]
            text = " ".join(splits[2:]).split()
            for word in text:
                if re.match('[0-9a-zA-Z]{5}', word):
                    word = word.encode().decode('unicode-escape')
                word = re.sub('(t[^A-Za-z0-9 ]|[^ ]*[0-9][^ ]*)', '', word)
                # if pf.censor(word) == "*"*len(word):
                #     yield word,server
                # if profaniti
                # doc = nlp(word)
                # if doc._.is_profane:
                #     yield word, server
                if len(word) > 0:
                    # if word in profanities:
                    #     yield word,server
                    yield word,server

                
    def combiner(self, word, serverTypes):
        serverTypes_set = set(serverTypes)
        for server in serverTypes_set:
            yield word, server
                    
    def reducer(self, word, serverTypes):
        serverTypes_list = list(set(serverTypes))
        if len(serverTypes_list) > 1:
            yield word, (len(serverTypes_list),serverTypes_list[:5])



if __name__ == '__main__':
    MRInvertedIndex.run()