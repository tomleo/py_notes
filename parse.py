import re
import pprint
class parseNotes(object):
    def __init__(self, file, *args, **kargs):
        self.elements=None
        self.main(file)

    def main(self, file_in):
        file_out = '{0}.html'.format(file_in.split('.')[:-1])
        with open(file_in) as file_in_obj:
            self.make_sections(file_in_obj)

    def make_sections(self, file_in_obj):
        #this might take up too much memory...
        temp = file_in_obj.read()
##TODO Need to edit regex so that it includes p elements - http://www.pythonregex.com/
        regex = re.compile("([h]{1}[1-9]{1}[:]{1}[\w\s\d]{1,};$)",re.MULTILINE)
        #r = regex.search(temp)
        pprint.pprint(regex.findall(temp))
                
            

if __name__ == '__main__':
    test = parseNotes('sample.n')
