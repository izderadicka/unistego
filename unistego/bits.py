'''
Created on Jan 4, 2014

@author: ivan
'''

import bitarray
import six

class BitsContainer(object):
    def __init__(self):
        self._bits=bitarray.bitarray()
        
    def size(self):
        return self._bits.length()
    
    __len__=size

class BitsReader(BitsContainer):
    def __init__(self, data, encoding='utf-8'):
        super(BitsReader,self).__init__()
        if not isinstance(data, six.binary_type):
            data=data.encode(encoding)
        self._bits.frombytes(data)
        
        self._index=0
        
    def remains(self):
        return self.size() - self._index
    
    def __next__(self):
        if self._index>=len(self._bits):
            raise StopIteration
        bit=self._bits[self._index]
        self._index+=1
        return bit
    next=__next__
        
    def __iter__(self):
        return self
    
class BitsWriter(BitsContainer):
    
    def write_bit(self, b):
        self._bits.append(b)
        
    def get_value(self):
        return self._bits.tobytes()

        
    