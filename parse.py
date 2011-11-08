import re
import pprint
class parseNotes(object):
    def __init__(self, file, *args, **kargs):
        self.elements=None
        self.main(file)
        self.master=None #A problem with this is that it will not be able to
                         #handle multiple elements, a muti-key dictionary would be nessisary 
                         #(or a named tupple?)

    def main(self, file_in):
        file_out = '{0}.html'.format(file_in.split('.')[:-1])
        with open(file_in) as file_in_obj:
            self.make_sections(file_in_obj)
        with open(file_out) as file_out_obj:
            self.make_html(file_out_obj)

    def make_sections(self, file_in_obj):
        file_string = file_in_obj.read()
        ##TODO Need to edit regex so that it includes p elements - http://www.pythonregex.com/
        #regex = re.compile("([h]{1}[1-9]{1}[:]{1}[\w\s\d]{1,};$)",re.MULTILINE)
        regex = re.compile("[h]{1}[1-9]{1}[:]|[p]{1}[:]")
        values = re.split(regex, file_string)
        values.pop(0) #this might be a bad idea...
        elements = re.findall(regex,file_string)
        self.master = dict((x[:-1], y.strip()[:-1]) for x, y in zip(elements,values))

    def make_html(self, file_out_obj):
        for element in self.master:
            self.format_html(element, self.master[element])

    def format_html(self, bun, meat):
        html_elements = {'h1': _h1,
                         'h2': _h2,
                         'h3': _h3,
                         'h4': _h4,
                         'h5': _h5,
                         'h6': _h6,
                         'h7': _h7,
                         'h8': _h8,
                         'h9': _h9,
                         'p': _p,
                         'code': _code
                         }
        #is there a way to pass values with an assosiative array?
        html_elements[bun]

    def _h1():
        pass

    def _h2():
        pass
    
    def _h3():
        pass

    def _h4():
        pass

    def _h5():
        pass

    def _h6():
        pass

    def _h7():
        pass

    def _h8():
        pass

    def _h9():
        pass

    def _p():
        pass

    def _code():
        pass


if __name__ == '__main__':
    test = parseNotes('sample.n')
