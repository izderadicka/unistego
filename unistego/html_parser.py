'''
Created on Jan 8, 2014

@author: ivan
'''

from six.moves import html_parser as parser  # @UnresolvedImport
from six.moves import html_entities as entities  # @UnresolvedImport

#from html import parser
#from html import entities
#from html.parser import  endendtag, endtagfind, tagfind_tolerant
from six import unichr
import copy
import logging
import six
log=logging.getLogger('unistego.html')


class Parser (parser.HTMLParser):
    def __init__(self,on_text_cb, on_markup_cb, fragment=False):
        parser.HTMLParser.__init__(self)
        self._on_text=on_text_cb
        self._on_markup=on_markup_cb
        self._tagstack=[]
        self._fragment=fragment
        
    def _is_text(self):
        if not self._fragment and not 'body' in self._tagstack:
            return False
        for name in ('script', 'style', 'math', 'svg'):
            if name in self._tagstack:
                return False
        return True
    
    def _text_out(self, data):
        if self._is_text():
            self._on_text(data)
        else:
            self._on_markup(data)
        
    def handle_data(self, data):
        if not isinstance(data, six.text_type):
            data=data.decode('utf-8')
        self._text_out(data)
        
    def handle_starttag(self, tag, attrs, ends=False):
        if not ends:
            self._tagstack.append(tag)
        self._on_markup(self.get_starttag_text())
        
    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == "</", "unexpected call to parse_endtag"
        match = parser.endendtag.search(rawdata, i+1) # >
        if not match:
            return -1
        gtpos = match.end()
        
        match = parser.endtagfind.match(rawdata, i) # </ + tag + >
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            if self.strict:
                self.error("bad end tag: %r" % (rawdata[i:gtpos],))
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = parser.tagfind_tolerant.match(rawdata, i+2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[i:i+3] == '</>':
                    return i+3
                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group().lower()
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after tha name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find('>', namematch.end())
            self.__end_tag_text=rawdata[i:gtpos+1]
            self.handle_endtag(tagname)
            return gtpos+1

        elem = match.group(1).lower() # script or style
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
        self.__end_tag_text=rawdata[i:gtpos]
        self.handle_endtag(elem.lower())
        self.clear_cdata_mode()
        return gtpos
    
    def get_endtag_text(self):
        return self.__end_tag_text
        
    def handle_endtag(self, tag):
        self._on_markup(self.get_endtag_text())  
        new_stack=copy.copy(self._tagstack)
        try:   
            while True:
                start_tag=new_stack.pop()
                if start_tag==tag:
                    self._tagstack=new_stack
                    break;
        except IndexError:
            log.warn('Missing start tag for end tag %s' % tag)
        
    def handle_comment(self, data):
        self._on_markup('<!--'+data+'-->')
        
    def handle_decl(self, decl):
        self._on_markup('<!'+decl+'>')
    
    def handle_pi(self, data):
        self._on_markup('<?'+data+'>')
        
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, ends=True)
        
    def handle_entityref(self, name):
        #we keep only basic SGML entities, rest is hadled and unicode text
        if name in ('quot', 'amp', 'apos', 'lt', 'gt'): 
            self._on_markup('&'+name+ ';')
        else:
            code=entities.name2codepoint.get(name)
            ch=None
            if code:
                ch=unichr(code)
            else:
                ch=entities.html5.get(name)
            if ch:
                self._text_out(ch)
            else:
                self._on_markup('&'+name+';')
                
    
    def handle_charref(self, name):
        if name.startswith('x'):
            ch=unichr(int(name[1:], 16))
        else:
            ch=unichr(int(name))
        self._text_out(ch)
        
    
        
        
        
    
        
        