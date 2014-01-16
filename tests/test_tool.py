'''
Created on Jan 15, 2014

@author: ivan
'''
import unittest
import subprocess
import os
import tempfile
from .test_streams import test_file
import six
import shutil
from .test_html import html_file2

root_dir=os.path.split(os.path.split(__file__)[0])[0]


class Test(unittest.TestCase):

    def setUp(self):
        self.tmp_dir=tempfile.mkdtemp( prefix='unistego')
        
    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        
    def test_tool(self):
        secret='Kulak brak burak honi prorchomet po metelici'
        tmp_file=os.path.join(self.tmp_dir, 'test.txt')
        self.call_proc([ '--hide', '--preset', 'joiners+zlib', '-o', tmp_file, 
                        '-m', secret, test_file])
        res=self.call_proc(['--unhide', '--preset', 'joiners+zlib', tmp_file],  )
        
        self.assertEqual(secret, res.decode('utf-8'))
        
    def test_tool2(self):
        secret='Kulak brak burak honi prorchomet po metelici'
        tmp_file=os.path.join(self.tmp_dir, 'test.html')
        self.call_proc([ '--hide', '--preset', 'spaces+zlib', '--html',  '-o', tmp_file, 
                        '--offset', '10000', '-m', secret, html_file2])
        res=self.call_proc(['--unhide', '--preset', 'spaces+zlib', '--html', tmp_file],  )
        
        self.assertEqual(secret, res.decode('utf-8'))
                
    def call_proc(self,  params):
        tmp_dir=tempfile.gettempdir()
        p=subprocess.Popen([os.path.join(root_dir,'bin/python3'), os.path.join(root_dir, 'unistego-tool.py'),]+params,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err=p.communicate()
        if err:
            self.fail('Process error output:\n'+err.decode('utf-8'))
            
        if p.returncode!= 0:
            self.fail('Process error code %d'%p.returncode)
        return out
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()