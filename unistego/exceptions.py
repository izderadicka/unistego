'''
Created on Jan 5, 2014

@author: ivan
'''


class StegoError(Exception):
    pass

class ErrorNotFinished(StegoError):
    pass

class ErrorIncompleteMessage(StegoError):
    pass
