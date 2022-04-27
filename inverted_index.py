from mrjob.job import MRJob
import re


class MRInvertedIndex(MRJob):
    def mapper(self, _, line):
        server = None
        if line.find("server: ") != -1:
            server = line[8:]
        if line.find("parsed_text: ") != -1:
            text = " ".join(line[8:]).split()
            for word in text:
                if re.match('[0-9a-zA-Z]{5}', word):
                    word = word.encode().decode('unicode-escape')
                word = re.sub('(t[^A-Za-z0-9 ]|[^ ]*[0-9][^ ]*)', '', word)
                if len(word) > 0:
                    yield word, server
                
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