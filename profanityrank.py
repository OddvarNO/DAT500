
from mrjob.job import MRJob
from mrjob.step import MRStep
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
# https://en.wikipedia.org/wiki/PageRank

PROFANE_WORDS = {'omorashi', 'blowjob', 'scat', 'snowballing', 'shitty', 'tits', 'tribadism', 'strap on', 'hot carl', 'wank', 'twat', 'zoophilia', 'spic', 'homoerotic', 'pisspig', 'jailbait', 'bastardo', 'shemale', 'xx', 'butthole', 'yaoi', 'kinkster', 'bastard', 'faggot', 'shit', 'frotting', 'beaner', 'baby juice', 'poontang', 'sultry women', 'female squirting', 'nigga', 'strapon', 's&m', 'gay sex', 'nudity', 'darkie', 'vibrator', 'genitals', 'male squirting', 'birdlock', 'date rape', 'double penetration', 'sucks', 'tub girl', 'rapist', 'urophilia', 'fisting', 'blumpkin', 'piece of shit', 'poop chute', 'nigger', 'poon', 'doggiestyle', 'rimjob', 'splooge', 'bullshit', 'ponyplay', 'yiffy', 'dvda', 'alabama hot pocket', 'beaver lips', 'double dong', 'donkey punch', 'slanteye', 'eat my ass', 'babeland', 'wetback', 'spread legs', 'bondage', 'nambla', 'feltch', 'masturbate', 'juggs', 'kinbaku', 'twinkie', 'bollocks', 'fucking', 'pedobear', 'beaners', 'dendrophilia', 'erotism', 'pussy', 'barenaked', 'queaf', 'porn', 'twink', 'knobbing', 'neonazi', 'raping', 'shitblimp', 'coon', 'blonde action', 'reverse cowgirl', 'spooge', 'girl on', 'acrotomophilia', 'porno', 'creampie', 'piss pig', 'doggie style', 'futanari', 'femdom', 'hentai', 'towelhead', 'god damn', 'topless', 'bangbros', 'sodomy', 'nig nog', 'bulldyke', 'black cock', 'clusterfuck', 'bukkake', 'felch', 'jigaboo', 'white power', 'boob', 'guro', 'rectum', 'doggy style', 'kinky', 'sexy', 'coprolagnia', 'undressing', 'muffdiving', 'blow job', 'dolcett', 'blonde on blonde action', 'shibari', 'punany', 'ass', 'tushy', 'anal', 'hooker', 'humping', 'dildo', 'wrinkled starfish', 'ball gag', 'gang bang', 'g-spot', 'pleasure chest', 'dry hump', 'camgirl', 'brown showers', 'anilingus', 'sodomize', 'bestiality', 'coons', 'carpetmuncher', 'schlong', 'auto erotic', 'lemon party', 'goatcx', 'intercourse', 'hand job', '2g1c', 'nude', 'domination', 'boner', 'boobs', 'make me come', 'kike', 'group sex', 'bimbos', 'how to kill', 'jail bait', 'fellatio', 'circlejerk', 'menage a trois', 'style doggy', 'queef', 'goodpoop', 'pissing', 'alaskan pipeline', 'panty', 'girls gone wild', 'tainted love', 'rosy palm and her 5 sisters', 'muff diver', 'autoerotic', 'goregasm', 'jack off', 'orgasm', 'dingleberry', 'bung hole', 'handjob', 'dirty sanchez', 'quim', 'mound of venus', 'pole smoker', 'rosy palm', 'big tits', 'big knockers', 'shrimping', 'threesome', 'poopchute', 'grope', 'strip club', 'two girls one cup', 'honkey', 'motherfucker', 'tongue in a', 'strappado', 'asshole', 'cornhole', 'goatse', 'jerk off', 'blue waffle', 'violet wand', 'deep throat', 'butt', 'dog style', 'camslut', 'dick', 'deepthroat', 'barely legal', 'fucktards', 'fuckin', 'dp action', 'arsehole', 'wrapping men', 'dominatrix', 'santorum', 'swastika', 'tight white', 'big breasts', 'jiggerboo', 'anus', 'upskirt', 'cunnilingus', 'titty', 'buttcheeks', 'doggystyle', 'bareback', 'playboy', 'nipple', 'camwhore', 'mr hands', 'big black', 'fingering', 'how to murder', 'brunette action', 'milf', 'cock', 'sadism', 'foot fetish', 'giant cock', 'phone sex', 'huge fat', 'penis', 'vagina', 'ejaculation', 'voyeur', 'shaved beaver', 'shota', 'pedophile', 'camel toe', 'jiggaboo', 'dommes', 'carpet muncher', 'busty', 'rimming', 'paedophile', 'suicide girls', 'orgy', 'nsfw images', 'escort', 'booty call', 'rape', 'bastinado', 'cunt', 'nipples', 'tied up', 'scissoring', 'titties', 'taste my', 'sex', 'spunk', 'cum', 'semen', 'baby batter', 'prince albert piercing', 'one cup two girls', 'urethra play', 'ecchi', 'fingerbang', 'missionary position', 'tubgirl', 'vorarephilia', 'jizz', 'nimphomania', 'wet dream', 'xxx', 'nympho', 'ball kicking', 'erotic', 'tit', 'golden shower', 'goo girl', 'blow your load', 'one guy one jar', 'ball sucking', 'assmunch', 'incest', 'pornography', 'coprophilia', 'lolita', 'poof', 'nymphomania', 'eunuch', 'cocks', 'fudge packer', 'pegging', 'pthc', 'hardcore', 'paki', 'jelly donut', 'tosser', 'panties', 'shaved pussy', 'bdsm', 'sexo', 'gokkun', 'venus mound', 'chocolate rosebuds', 'footjob', 'pubes', 'bitches', 'beaver cleaver', 'clitoris', '2 girls 1 cup', 'hard core', 'swinger', 'skeet', 'clover clamps', 'dirty pillows', 'ball licking', 'raging boner', 'ball sack', 'leather restraint', 'hot chick', 'throating', 'rusty trombone', 'splooge moose', 'bullet vibe', 'bunghole', 'fecal', 'suck', 'leather straight jacket', 'octopussy', 'vulva', 'tranny', 'slut', 'fuck buttons', 'snatch', 'girl on top', 'negro', 'dingleberries', 'bbw', 'cumming', 'tea bagging', 'ball gravy', 'nawashi', 'cleveland steamer', 'daterape', 'apeshit', 'lovemaking', 'raghead', 'fudgepacker', 'yellow showers', 'clit', 'smut', 'fuck', 'figging', 'bitch'}
ENGLISH_STOPWORDS = set(stopwords.words('english'))

class MRProfanityrank(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_profRank, mapper_init=self.mapper_profrank_init),
            # MRStep(mapper=self.mapper_createMatrix),
                   ]   

    def mapper_profrank_init(self):
        self.url = ""
        self.endUrl = ""
        self.links = ""
        self.profanityRank = 0
        self.allLinks = {}
        self.allprofanityRanks = {}
        self.count = 0

    def mapper_profRank(self, _, line):
        if line.find("url: ") == 0:
            self.url = line[line.find("/")+2:line[16:].find("/")+16]
            # self.url = line[5:]
            self.endUrl = line[5:]
            
        if line.find("links: {") == 0:
            self.links = line[8:line.find("}")]
            self.count += 1
        if line.find("parsed_text: ") == 0:
            text = line[12:]
            tokens = word_tokenize(text)
            
            # List comprehensions
            tokens = [word for word in tokens if not word in ENGLISH_STOPWORDS] # Removing stopwords
            pr = [word for word in tokens if word in PROFANE_WORDS] # gets all unique profane words in page
            tot_word = [word for word in tokens if not word in PROFANE_WORDS] # gets all non profane words in a page 

            # For loop version
            # remstop = []
            # pr = []
            # tot_word = []
            # for word in tokens:
            #     if not word in ENGLISH_STOPWORDS:
            #         remstop.append(word)
            #     if word in PROFANE_WORDS:
            #         pr.append(word)
            #     if not word in PROFANE_WORDS:
            #         tot_word.append(word)
            # tokens = remstop

            if len(tot_word) > 0 and len(set(pr)) > 0:
                self.profanityRank = (len(pr) / len(tot_word)) / (len(set(pr)) / len(PROFANE_WORDS)) 
                # self.profanityRank = (len(pr) + len(tot_word)) + (len(set(pr)) + len(PROFANE_WORDS)) 
                self.allLinks[self.url] = self.links
                self.allprofanityRanks[self.url] = self.profanityRank

            if self.endUrl == "https://zzsh111.com/a/Hu4SGefM/":                
                matrix = np.zeros((len(self.allLinks)+1, len(self.allLinks)+1))
                i, j = 0, 0 
                for url, links in self.allLinks.items():
                    for page in links.split(" "):
                        page = page[page.find("/")+2:page[1:].find("'") + 1]
                        # This if checks if a page is a key in the urls dictionary, and only then add to the matrix
                        if page in self.allLinks and url != page :
                            matrix[i][j] = (1 / len(self.allLinks[page]))  # This should have been 1/valid urls. 
                            j += 1
                    i += 1
                # Pagerank code copied from here: https://en.wikipedia.org/wiki/PageRank
                d = 0.85
                N = matrix.shape[1]
                v = np.random.rand(N, 1)
                v = v / np.linalg.norm(v, 1)
                M_hat = (d * matrix + (1 - d) / N)
                for _ in range(10):
                    v = M_hat @ v
                vlist = v.tolist()
                lengths = (len(vlist), len(self.allprofanityRanks), len(self.allLinks))

                yield (self.allprofanityRanks, self.count), (v.tolist(), lengths) 
        # Done to get only the websites with english language, as the profanities we use are only in english.
        if line.find("language: ") == 0:
            if line[10:] != "en" and self.url in self.allLinks and self.url in self.allprofanityRanks:
                self.allLinks.pop(self.url)
                self.allprofanityRanks.pop(self.url)
            self.url = ""
            self.profanityRank = 0

    def mapper_createMatrix(self, urls, ranks):
        matrix = np.zeros((len(urls)+1, len(urls)+1))
        i, j = 0, 0 
        for url, links in urls.items():
            for page in links.split(" "):
                page = page[page.find("/")+2:page[1:].find("'") + 1]
                # This if checks if a page is a key in the urls dictionary, and only then add to the matrix
                if page in urls and url != page :
                    matrix[i][j] = (1 / len(urls[page]))  # This should have been 1/valid urls. 
                    j += 1
            i += 1
        # Pagerank code copied from here: https://en.wikipedia.org/wiki/PageRank
        d = 0.85
        N = matrix.shape[1]
        v = np.random.rand(N, 1)
        v = v / np.linalg.norm(v, 1)
        M_hat = (d * matrix + (1 - d) / N)
        for _ in range(10):
            v = M_hat @ v
        vlist = v.tolist()
        # lengths = (len(vlist), len(ranks), len(urls))

        yield ranks, (vlist)    

if __name__ == '__main__':
    MRProfanityrank.run()