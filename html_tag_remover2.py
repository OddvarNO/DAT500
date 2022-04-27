from mrjob.job import MRJob
import warc

class MRRemoveHTMLTag(MRJob):

    def mapper(self, _, line):
        line = line.strip() # remove leading and trailing whitespace
        if line.find("From:") == 0:
            email_domain = line[line.find("@")+1:line.find(">")]
            if len(email_domain) == 0:
                email_domain == "empty"
            yield email_domain, line

    def combiner_old(self, key, values):
        yield key, sum(values)
        
    def reducer(self, key, values):
        arrayTest = []
        for x in values:
            arrayTest.append(x)
        yield key, arrayTest


if __name__ == '__main__':
    MRRemoveHTMLTag.run()