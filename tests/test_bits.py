# encoding=utf-8
'''
Created on Jan 4, 2014

@author: ivan
'''
import unittest
from unistego.bits import BitsReader, BitsWriter

class TestBits(unittest.TestCase):


    def test_reader(self):
        data=b'\xAA\xAA\xAA\xAA'
        bits=BitsReader(data)
        self.assertEqual(len(bits), 32)
        self.assertEqual(bits.remains(), 32)
        
        curr_bit=True
        count=0
        remains=32
        for b in bits:
            self.assertTrue(bool(curr_bit) == bool(b))
            count+=1
            remains-=1
            self.assertEqual(bits.remains(), remains)
            curr_bit=not curr_bit
        
        self.assertEqual(count, 32)
        
        
    def test_writer(self):
        bits=BitsWriter()
        curr_bit=True
        for i in range(32):
            bits.write_bit(curr_bit)
            curr_bit=not curr_bit
            
        self.assertEqual(len(bits), 32)
        self.assertEqual(bits.get_value(), b'\xAA\xAA\xAA\xAA')
        
        
        
    def test_both(self):
        text='Sedm lumpů šlohlo pumpu'
        r=BitsReader(text)
        w=BitsWriter()
        for b in r:
            w.write_bit(b)
            
        recovered_text=w.get_value().decode('utf-8')
        self.assertEqual(text, recovered_text)
        
            
        
        
            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_reader']
    unittest.main()