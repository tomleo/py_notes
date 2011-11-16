import sys
import re
import pprint

from pygments import highlight
from pygments.lexers import (guess_lexer, 
                             guess_lexer_for_filename,
                             get_lexer_by_name,
                             get_lexer_for_filename,
                             get_lexer_for_mimetype)
from pygments.formatters import HtmlFormatter

class parseNotes(object):
    def __init__(self, file, *args, **kargs):
        self.elements=None
        self.main(file)
        self.BR=None
        self.master=None

        self.struct

    def main(self, file_in):
        print "file_in: ", file_in
        file_out = '{0}.html'.format(file_in.split('.')[0])
        print "File out is: ", file_out
        self.BR=1
        with open(file_in) as file_in_obj:
            self.make_sections(file_in_obj)
        with open(file_out, "w") as file_out_obj:
            file_out_obj.write("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>PyParsed Note</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="code.css">
</head>
<body>
<div role="main" id="wrap">
""")
            self.make_html(file_out_obj)
            file_out_obj.write("</div></body></html>")

    def make_sections(self, file_in_obj):
        file_string = file_in_obj.read()
        # http://www.pythonregex.com/
        # http://docs.python.org/library/re.html
        # http://bytebaker.com/2008/11/03/switch-case-statement-in-python/
        #regex = re.compile("([h]{1}[1-9]{1}[:]{1}[\w\s\d]{1,};$)",re.MULTILINE)
        regex = re.compile("[h]{1}[1-9]{1}[:]|[p]{1}[s]{1}[:]|[p]{1}[:]|[c][o][d][e][<]")
        values = re.split(regex, file_string)
        values.pop(0) #this might be a bad idea...
        elements = re.findall(regex,file_string)
        self.master = list((x[:-1], y.strip()[:]) for x, y in zip(elements,values))
        pprint.pprint(self.master)

    def make_html(self, file_out_obj):
        for element in self.master:
            file_out_obj.write(self.format_html(element[0], element[1]))

    def format_html(self, bun, meat):
        html_headers = ('h1','h2','h2','h3','h4','h5','h6','h7','h8','h9')
        if bun in html_headers:
            #struct.add_header(meat)
            return "<{0}>{1}</{2}>\n".format(bun, meat, bun)
        elif 'ps' in bun:
            #child=struct.get_last(header).add_title(bun)
            ##ps=struct.get_last(header).append_ps(bun)
            ret = ""
            for line in meat.split('\n'):
                if '//#' in line:
                    l=line.split('//#')
                    #child.add_element(l[0], comment=l[1])
                    ##ps.append(l[0])
                    ret+='<p class="ps">{0}<span class="comment">{1}</span></p>\n'.format(l[0],l[1])
                else:
                    #child.add_element(line)
                    ##ps.append(l[0])
                    ret+='<p class="ps">{0}</p>\n'.format(line)
            return ret
        elif 'p' in bun:
            #struct.get_last(header).append_p(meat)
            if self.BR:
                meat=meat.split('\n')
                ret='<p>'
                for line in meat:
                    ret+=line+'<br />'
                ret+='</p>\n'
                return ret
            else:
                return '<p>{0}</p>'.format(meat)
        elif 'code' in bun:
            i = meat.find('>')
            lang = meat[:i]
            code = meat[i+2:-7] #-7 to remove endcode...
            #struct.get_last(header).append_code(lang, code)
            print "Get lexer by name"
            lang_=get_lexer_by_name(lang.lower())
            print lang_

            style_=HtmlFormatter(style='colorful').style
            format_=HtmlFormatter(style=style_)
            format_.noclasses = False
            format_.cssclass='code'
            format_.cssfile='code.css'
            return highlight(code, lang_, format_)
        else:
            print 'bun value was: ', bun

if __name__ == '__main__':
    test = parseNotes('sample.n')
