import unittest
import os
from pynif.dataset import NIFDataset
from .util import turtle_equal

class DatasetTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        testdir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(testdir, 'data/reuters-nif20.ttl'), 'r') as f:
            cls.example_nif20 = f.read()
        with open(os.path.join(testdir, 'data/reuters-nif21.ttl'), 'r') as f:
            cls.example_nif21 = f.read()
    
    def test_load_nif20(self):
        dataset = NIFDataset.loads(self.example_nif20)
        
        self.assertEqual(1, len(dataset.contexts))
        context = dataset.contexts[0]
        self.assertEqual(3, len(context.beans))
        
    def test_serialize_nif21(self):
        dataset = NIFDataset.loads(self.example_nif20)
        in_nif = dataset.dumps()
        with open('/tmp/a', 'w') as f:
            f.write(in_nif.decode('utf-8'))
        
        self.assertTrue(turtle_equal(self.example_nif21, in_nif))