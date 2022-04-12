from mrjob.job import MRJob

class MRRemoveHTMLTag(MRJob):
    def mapper_init(self):
        self.websiteAnServer = []
        self.in_body = False
        self.body = []
    
    def mapper(self, _, line):
        line = line.strip()
        if line.find('WARC-Target-URI: ') == 0:
            self.websiteAnServer.append(line[17:len(line)-1])
        
        if line.find('Server: ') == 0 :
            self.websiteAnServer.append(line[8:len(line)-1])
            
        if line.find('<body>') == 0 and not self.in_body:
            self.in_body=True
        
        if line.find("<p>") == 0:
            p_line = line[line.find("<p>")+3:line.find("</p>")]
            if len(p_line) == 0:
                p_line == "empty"
            self.body.append(p_line)

        if line.find('</body>') == 0 and self.in_body:
            yield (self.websiteAnServer[0],self.websiteAnServer[1]), ''.join(self.body)
            self.websiteAnServer = []
            self.body = []    
            self.in_body = False
        
        if self.in_body:
            self.body.append(line)


if __name__ == '__main__':
    MRRemoveHTMLTag.run()