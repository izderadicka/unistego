'''
Created on Jan 7, 2014

@author: ivan
'''
import unittest
import os
import subprocess
import six
import sys
import tempfile
from unistego.stream import get_hider, get_unhider, get_hider_html
from tests.test_streams import secret
from tests.test_html import html_file2

test_file=os.path.join(os.path.split(__file__)[0], 'text.txt')
if os.access('/usr/bin/ebook-convert', os.EX_OK):
    class ConversionError(Exception):
        pass
    class Convertor():
        def __init__(self, file_name):
            self._fname=file_name
        def convert(self,  output_file):
            
                
            p=subprocess.Popen(['/usr/bin/ebook-convert', self._fname, output_file],  stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            out, err=p.communicate()
            if err or p.returncode!=0:
                raise ConversionError('Error %d' % p.returncode)
                six.print_(err, file=sys.stderr)
            
            
            
    class TestConversion(unittest.TestCase):
    
        def test_conversion_spaceszlib(self):
            self.test_conversion('spaces+zlib')
        def test_conversion(self, preset='joiners'):
            tmp_dir=tempfile.mkdtemp(prefix='unistego_test_')
            in_file_name=os.path.join(tmp_dir,os.path.split(test_file)[-1])
            with open(test_file,'rt') as f:
                hider=get_hider(open(in_file_name, 'wt'), secret, preset )
                with  hider:
                    for l in f:
                        hider.write(l)
                    
            for ext in ['.epub', '.mobi', '.fb2', '2.txt']:
                in_file_ext=os.path.splitext(in_file_name)[1]
                out_file_name=os.path.splitext(in_file_name)[0]+ext
                c=Convertor(in_file_name)
                six.print_("Converting %s to %s" %(in_file_ext, ext))
                c.convert(out_file_name)
                in_file_name=out_file_name
                
            with get_unhider(open(in_file_name, 'rt'), preset) as unhider:
                
                while True:
                    t=unhider.read(1000)
                    if not t: 
                        break
                recovered_msg=unhider.get_message()
                
            self.assertEqual(secret, recovered_msg.decode('utf-8'))
            
        def test_conversion_html(self,preset='joiners'):
            tmp_dir=tempfile.mkdtemp(prefix='unistego_test_')
            in_file_name=os.path.join(tmp_dir,os.path.split(html_file2)[-1])
            with open(html_file2,'rt') as f:
                hider=get_hider_html(open(in_file_name, 'wt'), secret, preset )
                with  hider:
                    for l in f:
                        hider.write(l)
                    
            for ext in ['.epub', '.mobi', '.fb2', '.txt']:
                in_file_ext=os.path.splitext(in_file_name)[1]
                out_file_name=os.path.splitext(in_file_name)[0]+ext
                c=Convertor(in_file_name)
                six.print_("Converting %s to %s" %(in_file_ext, ext))
                c.convert(out_file_name)
                in_file_name=out_file_name
                
            with get_unhider(open(in_file_name, 'rt'), preset) as unhider:
                
                while True:
                    t=unhider.read(1000)
                    if not t: 
                        break
                recovered_msg=unhider.get_message()
                
            self.assertEqual(secret, recovered_msg.decode('utf-8'))
            
                
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_conversion']
    unittest.main()