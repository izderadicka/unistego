'''
Created on Jan 5, 2014

@author: ivan
'''

import zlib

class CompressStrategy(object):
    def __init__(self,  **kwargs):
        pass
    def compress(self, bytes_in):
        """compress input and return compressed bytes"""
        raise NotImplemented
        
    def decompress(self, bytes_in):
        """decompress input and return original message"""
        
    
class Zlib(CompressStrategy):
    def __init__(self,  **kwargs):
        self.level=kwargs.pop('level', 6)
        
    def compress(self, bytes_in):
        return zlib.compress(bytes_in, self.level)
    
    def decompress(self, bytes_in):
        return zlib.decompress(bytes_in)
    
        