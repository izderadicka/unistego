'''
Created on Jan 6, 2014

@author: ivan
'''
import unittest
import tests
from tests.test_streams import TestStreams
import cProfile as prof




if __name__ == "__main__":
    import sys;sys.argv = ['', 'TestStreams.test_streams']
    prof.run("unittest.main()", 'pstats')