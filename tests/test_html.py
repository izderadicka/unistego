'''
Created on Jan 9, 2014

@author: ivan
'''
import unittest
import os
import io
from unistego import html_parser
import six
from unistego import get_hider_html, get_unhider_html

from .test_streams import secret
html_file= os.path.join(os.path.split(__file__)[0], 'html1.html')
html_file2= os.path.join(os.path.split(__file__)[0], 'html2.html')
simple_html=six.u("""<!DOCTYPE html>
<html>
<head>
<title>Test Page</title>
</head>
<body>
<h1>My First Heading</h1>
<p>My first paragraph.</p>
</body>
</html>
""")
class Test(unittest.TestCase):


    def test_parser(self):
        out=io.StringIO()
        text=io.StringIO()
        
        def write_markup(data):
            out.write(data)
            
        def write_text(data):
            out.write(data)
            text.write(data)
            
        parser=html_parser.Parser(write_text, write_markup)
        
        for l in simple_html.splitlines(True):
            parser.feed(l)
        new_html=out.getvalue()
        #six.print_(new_html)
        self.assertEqual(new_html, simple_html)
        
        six.print_(text.getvalue())
        self.assertEqual(text.getvalue(), "\nMy First Heading\nMy first paragraph.\n")
        
    def test_parser2(self):
        out=io.StringIO()
        text=io.StringIO()
        
        def write_markup(data):
            out.write(data)
            
        def write_text(data):
            out.write(data)
            text.write(data)
            
        parser=html_parser.Parser(write_text, write_markup)
        with io.open(html_file, 'rt') as f:
            for l in f:
                parser.feed(l)
                
        #six.print_(out.getvalue())
        self.assertTrue(out.getvalue(), open(html_file,'rt').read())
        six.print_(text.getvalue())
        self.assertTrue(len(text.getvalue())>200)
        
    
    def test_hide(self, preset='joiners'):
        mstream=io.StringIO()
        hider=get_hider_html(mstream, secret, preset)
        with io.open(html_file2, 'rt') as f:
            for l in f:
                hider.write(l)
                
        with io.open('/tmp/test.html', 'wt') as out:
            out.write(mstream.getvalue())
            
        mstream=io.StringIO(mstream.getvalue())
        
        unhider=get_unhider_html(mstream, preset)
        
        for l in unhider:
            pass
        
        msg=unhider.get_message().decode('utf-8')
        
        self.assertEqual(msg,secret)
        
    def test_hide2(self):
        self.test_hide('spaces+zlib')
        
        

        
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()