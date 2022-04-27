from mrjob.job import MRJob
#from deep_translator import GoogleTranslator
#import deep_translator # import GoogleTranslator


class MRTranslate(MRJob):

    def mapper(self, _, line):
        line = line.strip() # remove leading and trailing whitespace
        if line != "":
            print(line)
#            translatedLine= deep_translator.GoogleTranslator(source="auto", targe t="en").translate(line)
#            translatedLine= GoogleTranslator(source="auto", target="en").translate("line")
#            print(translatedLine)
            yield line, 1

    def combiner(self, key, values):
        yield key, sum(values)
        
    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRTranslate.run()