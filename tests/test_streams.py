'''
Created on Jan 5, 2014

@author: ivan
'''
import unittest
import os
import io
from unistego.strategy import JoinersHidingStrategy, \
    JoinersUnhidingStrategy, AltSpaceHidingStrategy, AltSpaceUnhidingStrategy
from unistego.stream import HidingStream, UnhidingStream, PRESETS
from unistego import list_presets
import six
from unistego.compress import Zlib
import zlib

test_file=os.path.join(os.path.split(__file__)[0], 'text.txt')

secret="""The io module provides Python’s main facilities for dealing with various 
types of I/O. There are three main types of I/O: text I/O, binary I/O and raw I/O. 
These are generic categories, and various backing stores can be used for each of them. 
A concrete object belonging to any of these categories is called a file object. Other common terms are 
stream and file-like object."""

class TestStreams(unittest.TestCase):
    
    def test_list(self):
        names=list_presets()
        for n,help in names:
            self.assertTrue(PRESETS[n]['hider'])
            self.assertTrue(PRESETS[n]['unhider'])
    
    def test_compression_level(self):
        s=io.StringIO()
        try:
            hider=HidingStream(s, secret, JoinersHidingStrategy, Zlib, level=19)
            self.fail('Should fail on incorrect level')
        except zlib.error:
            pass

    def test_streams(self):
        _test_skeleton(self,{'strategy_class': JoinersHidingStrategy },
                             {'strategy_class':JoinersUnhidingStrategy, })
        
    def test_comressed(self):
        _test_skeleton(self,{'strategy_class': JoinersHidingStrategy, 'compress_class':Zlib, 'level':9 },
                             {'strategy_class':JoinersUnhidingStrategy, 'compress_class':Zlib })
        
    def test_spaces(self):
        _test_skeleton(self, {'strategy_class': AltSpaceHidingStrategy, 'compress_class':Zlib, 'level':9 },
                             {'strategy_class':AltSpaceUnhidingStrategy, 'compress_class':Zlib })
        
def _test_skeleton(self, hider_kwargs, unhider_kwargs):
    
   
    with io.open(test_file, 'rt') as f:
        text=f.read()
    mod_stream=io.StringIO()
    self.assertTrue(len(secret)*8 < JoinersHidingStrategy.analyze_capacity(text))
    hider=HidingStream(mod_stream, secret, **hider_kwargs)
    with io.open(test_file, 'rt') as f:
        while True:
            l=f.read(100)
            if not l:
                break
            hider.write(l)
    mod_stream=io.StringIO(mod_stream.getvalue())
    hider.close()    
    self.assertEqual(hider.remains_to_hide(), 0)
    mod_text=mod_stream.getvalue()
    self.assertTrue(unhider_kwargs['strategy_class'].test_text(mod_text))
    
    with UnhidingStream(mod_stream, **unhider_kwargs) as unhider:
        lines=0
        for l in unhider:
            #six.print_(l)
            lines+=1
            if lines==200:
                break
        while True:
            l=unhider.read(99)
            if not l:
                break
            
    self.assertTrue(lines>100)
        
    msg=unhider.get_message().decode('utf-8')
    
    self.assertEqual(secret, msg)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()