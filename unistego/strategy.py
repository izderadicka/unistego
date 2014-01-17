'''
Created on Jan 4, 2014

@author: ivan
'''
from .bits import BitsReader, BitsWriter
import re
import unicodedata
from unistego.exceptions import StegoError, ErrorIncompleteMessage
from unistego.utils import is_word_char
import random
import six


class HidingStrategy(object):
    def __init__(self, secrect_message, **kwargs):
        self._msg=secrect_message
        self._bits=BitsReader(secrect_message)
        self._done=False
        self._started=False
        
    def hide(self, text):
        """Hides bytes in text, returns text with some part of hidden message"""
        if not self._done:
            res=[]
            for i,ch in enumerate(text):
                if  self._done:
                    res.append(ch)
                else:
                    self.hide_one(res, ch, i)
                
            return self.results_to_text(res)
        else:
            return text
        
    def hide_one(self, result, ch, pos):
        """hides one piece or just progress forward, characters  should be appended to result"""
        raise NotImplemented
    
    def results_to_text(self,res):
        """ Converts list of charactes to resulting text"""
        return ''.join(res)
    
    def read_next_bit(self):
        try:
            return next(self._bits)
        except StopIteration:
            self._done=True
            return None
        
        
    def flush(self):
        """Returns any remaining part of text, if any"""
    
    @property
    def remaining_bits(self):
        """ How much bits is still to be hidden in text"""
        return self._bits.remains()
        
    @staticmethod    
    def analyze_capacity(all_text):
        """Return maximum estimated number of bits that can be hidden in given text"""
        raise NotImplemented

class UnhidingStrategy(object):
    def __init__(self, **kwargs):
        self._bits=BitsWriter()
        self._done=False
        self._started=False
    def get_message(self, force=False):
        """ returns hidden message, after processing all text"""
        if not self._done and not force:
            raise ErrorIncompleteMessage('Message is not complete')
        return self._bits.get_value()
    def unhide(self,text):
        """process text with hidden info"""
        raise NotImplemented
        
    @staticmethod    
    def test_text(text):
        """ returns true if text contains hidden message (at least begining of the message)"""
        raise NotImplemented
        
class _TextStatus(object):
    def __init__(self):
        self._prev_char=None
        self._curr_char=None
        self._done=False
        self._started=False
    def update(self, ch): 
        self._prev_char=self._curr_char 
        self._curr_char=ch
    def can_insert(self):  
        if not self._prev_char or not self._curr_char:
            return False
        if is_word_char(self._prev_char) and   is_word_char(self._curr_char):
            return True
    def prev_char(self):
        return self._prev_char

     
class JoinersHidingStrategy(HidingStrategy):
    CHAR_ZERO=unicodedata.lookup('ZERO WIDTH NON-JOINER') 
    CHAR_ONE=unicodedata.lookup('ZERO WIDTH JOINER')     
    def __init__(self, secret_message, **kwargs):
        self._space_between=kwargs.pop('fill_factor', 1)
        self._next_hit=1
        super(JoinersHidingStrategy, self).__init__(secret_message)
        self._state=_TextStatus()
        
    def hide_one(self, res, ch, pos):
        if ch in [self.CHAR_ZERO, self.CHAR_ONE]:
            raise StegoError('Carrier text contains Zero Width Joiners')
        self._state.update(ch)
        if self._state.can_insert():
            if not self._started:
                res.append(self.CHAR_ZERO)
                res.append(self.CHAR_ONE)
                self._started=True
                self._calc_next_hit()
            elif self._next_hit<=1:
                b=self.read_next_bit()
                if b is not None:
                    if b:
                        bit_char=self.CHAR_ONE
                    else:
                        bit_char=self.CHAR_ZERO
                    res.append(bit_char)
                else:
                    res.append(self.CHAR_ONE)
                    res.append(self.CHAR_ZERO)
                    self._done=True
                self._calc_next_hit()
            else:
                self._next_hit-=1
        res.append(ch)
        
    def _calc_next_hit(self):
        if  isinstance(self._space_between, int):
            self._next_hit=self._space_between
        elif isinstance(self._space_between, (tuple,list)) and len(self._space_between)==2:
            self._next_hit=random.randint(self._space_between[0], self._space_between[1])
        else:
            raise ValueError('Fill factor must be either integer ot tuple of two integers')
            
        
            
        
        
    @staticmethod
    def analyze_capacity(all_text):
        count=0
        state=_TextStatus()
        for ch in all_text:
            state.update(ch)
            if state.can_insert():
                count+=1
        return count
                
        
class JoinersUnhidingStrategy(UnhidingStrategy):
    def __init__(self, **kwargs):
        super(JoinersUnhidingStrategy, self).__init__( **kwargs)
        self._state=_TextStatus()
        self._deferred_bit=False
    
    def unhide(self, text):
        if self._done:
            return
        for ch in text:
            self._state.update(ch)
            if self._started:
                if ch==JoinersHidingStrategy.CHAR_ZERO:
                    if self._state.prev_char()==JoinersHidingStrategy.CHAR_ONE:
                        self._done=True
                        break
                    self._bits.write_bit(0)
                elif ch==JoinersHidingStrategy.CHAR_ONE:
                    self._deferred_bit=True
                elif self._deferred_bit:
                    self._bits.write_bit(1)
                    self._deferred_bit=False
            else:
                if ch==JoinersHidingStrategy.CHAR_ONE and \
                self._state.prev_char()==JoinersHidingStrategy.CHAR_ZERO:
                    self._started=True
                
        
    
    @staticmethod
    def test_text(text):
        for ch in text:
            if  ch==JoinersHidingStrategy.CHAR_ZERO or ch==JoinersHidingStrategy.CHAR_ZERO:
                return True

class _TextStatusExt(object):   
    def __init__(self):    
        self._history=[]   
        self._history_len=3
    def update(self, ch): 
        self._history.append(ch)  
        if len(self._history)>self._history_len:
            self._history.pop(0)
    def can_insert(self):
        if len(self._history)<self._history_len:
            return False
        if is_word_char(self._history[-3]) and   is_word_char(self._history[-1]) and \
            self.is_space(self._history[-2]):
            return True
    def is_space(self, ch):
        return ch in (AltSpaceHidingStrategy.CHAR_SPACE, AltSpaceHidingStrategy.CHAR_SPACE1, 
                                  AltSpaceHidingStrategy.CHAR_SPACE2)
    def get_prev_char(self):
        if len(self._history)>1:
            return self._history[-2]
    def reset(self):
        self._history=[]
        
        
class UnfinishedString(six.text_type):
        pass
        
           
class AltSpaceHidingStrategy(HidingStrategy):    
    CHAR_SPACE=unicodedata.lookup('SPACE')
    CHAR_SPACE1=unicodedata.lookup('FOUR-PER-EM SPACE')  
    CHAR_SPACE2=unicodedata.lookup('THREE-PER-EM SPACE') 
    
    def __init__(self, secrect_message, **kwargs):
        HidingStrategy.__init__(self, secrect_message, **kwargs)
        self._state=_TextStatusExt()
        self._delayed_char=None
        self._delayed_cb=kwargs.pop('delayed_cb', None)
        self._unfinished=None
        
    def _resolve_delayed(self, pos, next_text, ch=None):
        if not ch:
            ch=self._delayed_char
        if self._delayed_cb and pos==0:
            self._delayed_cb(ch) # handling delayed character from previous call
        else:
            next_text.append(ch)
        self._delayed_char=None
        
    def hide_one(self, res, ch, pos):
        self._state.update(ch)
        if self._state.can_insert():
            if not self._started:
                self._resolve_delayed(pos, res, self.CHAR_SPACE2)
                self._started=True
            else:
                b=self.read_next_bit()
                if not b is None:
                    if b:
                        self._resolve_delayed(pos, res, self.CHAR_SPACE)
                    else:
                        self._resolve_delayed(pos, res, self.CHAR_SPACE1)
                else:
                    self._resolve_delayed(pos, res, self.CHAR_SPACE2)
                    self._state.reset()
                
        else:
            if self._delayed_char:
                self._resolve_delayed(pos,res)
            
            if self._state.is_space(ch):
                self._delayed_char=ch
                return
        res.append(ch)
        
    def results_to_text(self, res):
        text=''.join(res)
        if self._delayed_char:
            self._unfinished= UnfinishedString(text)
            return self._unfinished
        else:
            self._unfinished=None
            return text
        
    def flush(self):
        return self._delayed_char
    
    @staticmethod
    def analyze_capacity(all_text):
        if not isinstance(all_text , six.text_type):
            raise ValueError('Input must be unicode text')
        count=0
        state=_TextStatusExt()
        for ch in all_text:
            state.update(ch)
            if state.can_insert():
                count+=1
        return count-2
    
    
class AltSpaceUnhidingStrategy(UnhidingStrategy):
    
    def __init__(self, **kwargs):
        UnhidingStrategy.__init__(self, **kwargs)
        self._state=_TextStatusExt()
        
    def unhide(self, text):
        if self._done:
            return
        for ch in text:
            self._state.update(ch)
            if self._state.can_insert():
                if self._done:
                    break
                prev=self._state.get_prev_char()
                if self._started and prev==AltSpaceHidingStrategy.CHAR_SPACE:
                    self._bits.write_bit(1) 
                elif self._started and prev==AltSpaceHidingStrategy.CHAR_SPACE1:
                    self._bits.write_bit(0)
                elif prev==AltSpaceHidingStrategy.CHAR_SPACE2:
                    if not self._started:
                        self._started=True
                    else:
                        self._done=True
                    
    @staticmethod
    def test_text(all_text):
        iterator=iter(all_text)
        found_space=0
        try:
            while True:
                ch=next(iterator) 
                if found_space==1 and ch==AltSpaceHidingStrategy.CHAR_SPACE1:
                    found_space=2
                elif found_space==2 and ch==AltSpaceHidingStrategy.CHAR_SPACE2:
                    return True
                elif found_space==0 and ch==AltSpaceHidingStrategy.CHAR_SPACE2:
                    found_space=1
        except StopIteration:
            pass
            
          
        
        
    
  
        
    
