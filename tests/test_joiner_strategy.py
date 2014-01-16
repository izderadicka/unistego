'''
Created on Jan 4, 2014

@author: ivan
'''
import unittest
from unistego import strategy
import os
import io
from unistego.strategy import JoinersHidingStrategy, JoinersUnhidingStrategy
import six

test_file=os.path.join(os.path.split(__file__)[0], 'text.txt')
class TestJoinerStrategy(unittest.TestCase):


    def test_hide(self):
        secret = "tajna zprava"
        text= io.open(test_file, mode='rt', encoding='utf-8').read(2000)
        hider=strategy.JoinersHidingStrategy(secret)
        text2=hider.hide(text)
        six.print_(text2)
        self.assertTrue(len(text2)==len(text)+len(secret)*8+4)
        
        
    def test_capacity(self):
        text=io.open(test_file, mode='rt', encoding='utf-8').read()
        size=len(text)
        capacity=JoinersHidingStrategy.analyze_capacity(text)
        six.print_('Relative capacity:', capacity/size)
        self.assertTrue(capacity> size/2 and capacity<size)
        
    def test_both(self):
        secret = "tajna zprava"
        text= io.open(test_file, mode='rt', encoding='utf-8').read(2000)
        hider=strategy.JoinersHidingStrategy(secret)
        text2=hider.hide(text)
        unhider=JoinersUnhidingStrategy()
        unhider.unhide(text2)
        text3=unhider.get_message().decode('utf-8')
        self.assertEqual(secret, text3)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()