import sys
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
        print "file_in: ", file_in
        file_out = '{0}.html'.format(file_in.split('.')[0])
        print "File out is: ", file_out
        with open(file_in) as file_in_obj:
            self.make_sections(file_in_obj)
        with open(file_out, "w") as file_out_obj:
            file_out_obj.write("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>PyParsed Note</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div role="main" id="wrap">
""")
            self.make_html(file_out_obj)
            file_out_obj.write("</div></body></html>")

    def make_sections(self, file_in_obj):
        file_string = file_in_obj.read()
        ##TODO Need to edit regex so that it includes p elements
            # http://www.pythonregex.com/
            # http://docs.python.org/library/re.html
            # http://bytebaker.com/2008/11/03/switch-case-statement-in-python/
        #regex = re.compile("([h]{1}[1-9]{1}[:]{1}[\w\s\d]{1,};$)",re.MULTILINE)
        regex = re.compile("[h]{1}[1-9]{1}[:]|[p]{1}[s]{1}[:]")
        values = re.split(regex, file_string)
        values.pop(0) #this might be a bad idea...
        elements = re.findall(regex,file_string)
        print "values: ", values
        print "elements: ", elements
        self.master = list((x[:-1], y.strip()[:-1]) for x, y in zip(elements,values))

    def make_html(self, file_out_obj):
        for element in self.master:
            file_out_obj.write(self.format_html(element[0], element[1]))

    def format_html(self, bun, meat):
        html_headers = ('h1','h2','h2','h3','h4','h5','h6','h7','h8','h9')
        if bun in html_headers:
            return "<{0}>{1}</{2}>\n".format(bun, meat, bun)
        elif 'p' in bun:
            ret = ""
            for line in meat.split('\n'):
                if '//#' in line:
                    l=line.split('//#')
                    ret+='<p class="ps">{0}<span class="comment">{1}</span></p>\n'.format(l[0],l[1])
                else:
                    ret+='<p class="ps">{0}</p>\n'.format(line)
            return ret
        elif bun is 'code':
            pass
        else:
            print 'bun value was: ', bun

        #is there a way to pass values with an assosiative array?
        #html_elements[bun]()


if __name__ == '__main__':
    test = parseNotes('sample.n')
