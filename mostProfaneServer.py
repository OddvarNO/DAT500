
from gettext import find
from mrjob.job import MRJob
import re

class MRMostProfaneServer(MRJob):
    def mapper_init(self):
        self.server = ""
        self.amountOfProfanities = ""

    def mapper(self, _, line):
        if line.find("server: ") == 0:
            self.server = re.sub("[\].*$", "", line[8:])
            # if self.server.find("Apache") == 0:
            #     self.server == self.server[:5]
            # else if self.server.find()
        if line.find("profanity_prob: ") == 0:
            self.amountOfProfanities = line[16:]
            if int(self.amountOfProfanities) != 0:
                yield self.server, 1
            self.server = ""
            self.amountOfProfanities = ""
    
    def combiner(self, key, values):
        yield key, sum(values)
        
    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRMostProfaneServer.run()