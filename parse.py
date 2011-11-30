#/usr/bin/python3

import sys
import re
import pprint

from pygments import highlight
from pygments.lexers import (get_lexer_by_name,
                             get_lexer_for_filename,
                             get_lexer_for_mimetype,
                             RegexLexer,
                             DelegatingLexer
                             )
from pygments.formatters import HtmlFormatter
#from pygments.lexer import RegexLexer
from pygments.token import *

class DOM(list):

    def __init__(self, title=None):
        self.title=title
        self.objects=[]

    def append(self, obj):
        self.objects.append(obj)

class Element(object):

    def __init__(self, name_):
        #self.type_=type_
        self.name_=name_

class Header(Element):

    def __init__(self, name_, type_):
        self.type_=type_
        self.children=[]
        super().__init__(name_)

    def add_child(self, obj):
        self.children.append(obj)

    def get_html(self, andChildren=False):
        head="<{0}>{1}</{0}>".format(self.type_, self.name_)
        if andChildren:
            html=[]
            for child in children:
               html.append(child.get_html)
               return '\n'.join(html.insert(head))
        else:
            return head

class P(Element):

    def __init__(self, content_, br_=True):
        self.content_=content_
        self.comments_=[]
        self.br_=br_
        super().__init__(name_="")

    def get_html(self):
        html=['<p>']
        if self.br_:
            lines=self.content_.split('\n')
            for line in lines:
                if '//#' in line:
                    l=line.split('//#')
                    temp='{0} <span class="comments">{1}</span>'.format(l[0],l[1])
                    html.append(temp)
                else:
                    html.append(line)
                html.append('<br />\n')
        #No support for comments in paragraphs that are not seperated by \n's
        #unless everything after //# should be interpreted as a comment...
            html.append('</p>')
            return '\n'.join(html)
        else:
            html.append(self.content_)
            html.append('</p>')
            return '\n'.join(html)

class Ps(Element):
     
    def __init__(self, content_=None, comments_=None):
        if content_:
            self.content_=content_
        else:
            self.content_=[]
        if comments_:
            self.comments_=comments_
        else:
            self.comments_=[]
        name_=""
        super().__init__(name_)

    def add_line(self, line, comment=None):
        self.content_.append(line)
        if comment:
            self.comments_.append(comment)
        else:
            self.comments_.append(None)

    def get_html(self):
        html=[]
        for i, line in enumerate(self.content_):
            if self.comments_[i]:
                #html.append('<p class="ps">{0} <span class="comments">{1}</span></p>'.format(line,
                #                                                                    self.comments_[i]))
                #html.append('<p class="ps"> {0} <a href="#" title="Comment">{1}</a></p>'.format(line, self.comments_[i]))
                html.append('<p class="ps"><a href="#" title="{1}">{0}</a></p>'.format(line, self.comments_[i]))
            else:
                html.append('<p class="ps"> {0} </p>'.format(line))
        return '\n'.join(html)


"""
The idea behind creating a custom lexer is that
it is impossible to know what line a comment came from if you
filter it out before the code is converted to html.

When code is converted to html, pygments also attempts
to highlight the //# comments which I wish to remove

An alternate to creating custom lexer's might be to
create a custom filter http://pygments.org/docs/filters/
"""
#a better implementation might be with Callbacks, see pygments documentation
# http://pygments.org/docs/lexerdevelopment/#callbacks
class CustomLexer(DelegatingLexer):
    def __init__(self, lex_type, **options):
        super(lex_type, self).__init__(Comment_Lex, lex_type, **options)

class NoteLexer(ExtededRegexLexer):

    def comment_callback(lexer, match, ctx):
        comment=match.group(1)
        text=match.group(2)
        yeild match.start(), Generic.Headline, comment + text
        ctx.pos = match.end()

    tokens = {
        'root': [
            ('[/]{2}[#].+', headline_callback)
        ]
    }

#TODO Read into creating a filter for the //# comments/asides
#    1. Possibly rename comments
class Code(Element):

    def __init__(self, lang_, code_, name_=""):
        self.lang_=lang_
        self.code_=code_
        self.comments_=[]
        #codelen1=len(self.code_)#
        #if '//#' in self.code_:
        #    self.pull_comments()
        #else:
        #    self.comments_=[None for i in code_]
        #codelen2=len(self.code_)#
        #print("before: ", codelen1, " after: ", codelen2)
        super().__init__(name_)

    def pull_comments(self):
        #print("1. len of code: ", len(self.code_))
        self.code_=self.code_.split('\n')
        for i, line in enumerate(self.code_):
            if '//#' in line:
                cline = line.split('//#')
                self.comments_.insert(i, cline[1])
                self.code_[i]=cline[0]
                #print ("line after pull: ", self.code_[i])
                #print ("len of code: ", len(self.code_))
                #exit()
            else:
                self.comments_.insert(i, None)
        #print("Live from pull_comments()")
        #print("Code length: ", len(self.code_))
        #print("Comment length: ", len(self.comments_))
        self.code_='\n'.join(self.code_)
        #print("2. len of code: ", len(self.code_))
        #print("\n")

    def test_html_parse(self, style_='colorful'):
        lex=get_lexer_by_name(self.lang_.lower())
        for token in lex.get_tokens(self.code_):
            print(token)

    #Need to find a way to insert 'a' tag into the content of code after it has
    #been rendered into html code, also don't want the a tag to wrap block
    #elements as that would not be valid html
    #
    #the line numbers are destoryed when code is translated
    #searching for a segment can be hard because they are split by html tags
    # pygments attempts to highlight //# so the best way would be to
    # modify pygments highlighting function to ignore //# so that tags
    def get_html(self, style_='colorful'):
        #Pygments configuration
        lex=get_lexer_by_name(self.lang_.lower())
        htmlFormat=HtmlFormatter(style=style_)
        htmlFormat.noclasses=False
        htmlFormat.cssclass='code'
        htmlFormat.cssfile='code.css'

        html=highlight(self.code_, lex, htmlFormat)
      
        #self.code_=self.code_.split('\n')
        #assert(len(self.code_)==len(self.comments_))
        #print("About to enter the get_html() function forloop")
        #for i, line in enumerate(self.code_):
        #    if self.comments_[i]:
        #        #tmp=list(html.partition(self.code_[i]))
        #        tmp=list(html.partition('<pre>'))
        #        print("1. ", tmp)
        #        before='<a href="#" title="{0}">'.format(self.comments_[i])
        #        tmp.insert(2, before)
        #        print("2. ", tmp)
        #        after='</a>'
        #        tmp.insert(3, after)
        #        html=''.join(tmp)
        #        print("3. ", tmp)
        
        # re.I = ignore case
        # re.S = dotall

        """html2=html.split('\n')
        print("length of html2: ", len(html2))
        print("length of comments: ", len(self.comments_))
        for i, line in enumerate(html2[:]):
            if self.comments_[i]:
                pattern = re.compile('<pre>(.*?)</pre>', re.I | re.S)
                temp=pattern.split(line)
                temp.insert(1, '<a href="#" title={0}">'.format(self.comments_[i]))
                temp.insert(4, '</a>')
        #html2.join('\n')
        '\n'.join(html2)"""

         
        #for i, each in enumerate(pattern.split(html)):
        #    print(i, " ", each)
           
        return html
       


class parseNotes(object):
    def __init__(self, file_, *args, **kargs):
        self.elements_=None
        self.main(file_)
        
        self.BR=None
        self.master=None

        self.DOM_=None

    def main(self, file_in):
        file_=file_in.split('.')[0]
        file_out='{0}.html'.format(file_)
        self.BR=1
        self.DOM_=DOM()
        print("FILE IN:  ", file_in)
        print("FILE OUT: ", file_out)
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
<link rel="stylesheet" href="tooltips.css">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script>
<script src="tooltips.js"></script>
<script>
$(function() { $(".ps a[title]").tooltips();  });
</script>
</head>
<body>
<div role="main" id="wrap">
""")
            self.make_html(file_out_obj)
            file_out_obj.write("</div></body></html>")

    def make_sections(self, file_in_obj):
        file_string = file_in_obj.read()
        regex = re.compile("[h]{1}[1-9]{1}[:]|[p]{1}[s]{1}[:]|[p]{1}[:]|[c][o][d][e][<]")
        values = re.split(regex, file_string)
        values.pop(0) #this might be a bad idea...
        elements = re.findall(regex,file_string)
        self.master = list((x[:-1], y.strip()[:]) for x, y in zip(elements,values))
        assert(self.master)
        #pprint.pprint(self.master)

    def make_html(self, file_out_obj):
        for element in self.master:
            elem_type=element[0]
            elem_val=element[1]
            file_out_obj.write(self.format_html(elem_type, elem_val))

    def format_html(self, bun, meat):
        html_headers = ('h1','h2','h2','h3','h4','h5','h6','h7','h8','h9')
        if bun in html_headers:
            head=Header(meat,bun)
            self.DOM_.append(head)
            return head.get_html()
        elif 'ps' in bun:
            ps=Ps()
            for line in meat.split('\n'):
                if '//#' in line:
                    l=line.split('//#')
                    ps.add_line(l[0], comment=l[1])
                else:
                    ps.add_line(line)
            return ps.get_html()
        elif 'p' in bun:
            return P(meat).get_html()
        elif 'code' in bun:
            i = meat.find('>')
            lang = meat[:i]
            code = meat[i+2:-7] #-7 to remove endcode...
            #style_=HtmlFormatter(style='colorful').style
            #format_=HtmlFormatter(style=style_)
            c=Code(lang, code).get_html()
            #c=Code(lang, code).test_html_parse()
            return c
        else:
            pass
            #print ('bun value was: ', bun)


if __name__ == '__main__':
    test = parseNotes('sample.n')
