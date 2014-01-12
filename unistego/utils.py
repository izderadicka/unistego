'''
Created on Jan 6, 2014

@author: ivan
'''

import unicodedata as uni

WORD_CHAR_CATS=['Ll', 'Lu', 'Lt', 'Lo', 'Lm', 'Nd', 'Pc']
def is_word_char(ch):
    return uni.category(ch) in WORD_CHAR_CATS