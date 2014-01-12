'''
Created on Jan 6, 2014

@author: ivan
'''
import unittest
from unistego.strategy import AltSpaceHidingStrategy, AltSpaceUnhidingStrategy
import six
import os
import io

test_file=os.path.join(os.path.split(__file__)[0], 'text.txt')
class TestSpacesStrategy(unittest.TestCase):


    def test_capacity(self):
        with open(test_file,'rt') as f:
            text=f.read()
        capacity=AltSpaceHidingStrategy.analyze_capacity(text)
        rel_capacity=capacity/len(text)
        six.print_('Relative capacity: ', rel_capacity)
        self.assertTrue(rel_capacity>0.1)
        
    def test_hide(self):
        secret = "tajna zprava"
        text= io.open(test_file, mode='rt', encoding='utf-8').read(2000)
        hider=AltSpaceHidingStrategy(secret)
        text2=hider.hide(text)
        self.assertEqual(hider.remaining_bits, 0)
        six.print_(text2.encode('utf-8'))
        self.assertTrue(len(text2)==len(text))
        self.assertTrue(len(text2.encode('utf-8'))> len(text.encode('utf-8'))+70)
        
        
    def test_both(self):
        secret = "tajnejsi zprava"
        text_file= io.open(test_file, mode='rt', encoding='utf-8')
        hider=AltSpaceHidingStrategy(secret)
        text2=io.StringIO()
        for i in range(200):
            text2.write(hider.hide(text_file.read(10)))
        unhider=AltSpaceUnhidingStrategy()
        unhider.unhide(text2.getvalue())
        text3=unhider.get_message().decode('utf-8')
        self.assertEqual(secret, text3)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()