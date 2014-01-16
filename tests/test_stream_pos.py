'''
Created on Jan 13, 2014

@author: ivan
'''
import unittest
from unistego.strategy import JoinersHidingStrategy, JoinersUnhidingStrategy,\
    AltSpaceHidingStrategy, AltSpaceUnhidingStrategy
from .test_streams import _test_skeleton    
from unistego.compress import Zlib
import io
from unistego.stream import get_hider_html, get_unhider_html
from tests.test_html import html_file2
from tests.test_streams import secret




class TestStreamPos(unittest.TestCase):


    def test_joiners(self):
        _test_skeleton(self,{'strategy_class': JoinersHidingStrategy, 'start_at':300000 },
                             {'strategy_class':JoinersUnhidingStrategy, 'start_at':300000})
        
    def test_joiners_spares(self):
        _test_skeleton(self,{'strategy_class': JoinersHidingStrategy, 'start_at':30000, 'fill_factor':(5,10) },
                             {'strategy_class':JoinersUnhidingStrategy, 'start_at':30000})
    
    def test_spaces(self):
        _test_skeleton(self, {'strategy_class': AltSpaceHidingStrategy, 'compress_class':Zlib, 'level':9, 'start_at':99999 },
                             {'strategy_class':AltSpaceUnhidingStrategy, 'compress_class':Zlib })
        
    def test_html(self, preset='joiners', hiding_pos=444000, unhiding_pos=0, **kwargs):
        mstream=io.StringIO()
        hider=get_hider_html(mstream, secret, preset, start_at=hiding_pos, **kwargs)
        with open(html_file2, 'rt') as f:
            for l in f:
                hider.write(l)
                
        with open('/tmp/test.html', 'wt') as out:
            out.write(mstream.getvalue())
            
        mstream=io.StringIO(mstream.getvalue())
        unhider=get_unhider_html(mstream, preset, start_at=unhiding_pos, **kwargs)
        for l in unhider:
            pass
        msg=unhider.get_message().decode('utf-8')
        
        self.assertEqual(msg,secret)
        
        
    def test_html2(self):
        self.test_html(preset='spaces', hiding_pos=23333, unhiding_pos=23333)
        
    def test_html3(self):
        self.test_html(preset='joiners', hiding_pos=23333, unhiding_pos=23333, fill_factor=(5,10))
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()