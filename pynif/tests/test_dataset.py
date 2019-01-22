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
        with open(os.path.join(testdir, 'data/reuters-nif20-normalized.ttl'), 'r') as f:
            cls.example_nif20_normalized = f.read()
        with open(os.path.join(testdir, 'data/reuters-nif21.ttl'), 'r') as f:
            cls.example_nif21 = f.read()
        with open(os.path.join(testdir, 'data/example-maradona.ttl'), 'r') as f:
            cls.example_maradona = f.read()
    
    def test_serialize_nif21(self):
        dataset = NIFDataset.loads(self.example_nif21)
        
        self.assertEqual(1, len(dataset.contexts))
        context = dataset.contexts[0]
        self.assertEqual(3, len(context.beans))
        
        in_nif = dataset.dumps()
        
        self.assertTrue(turtle_equal(self.example_nif21, in_nif))
        
    def test_serialize_nif20(self):
        dataset = NIFDataset.loads(self.example_nif20)
        
        self.assertEqual(1, len(dataset.contexts))
        context = dataset.contexts[0]
        self.assertEqual(3, len(context.beans))
        
        in_nif = dataset.dumps()
        
        self.assertTrue(turtle_equal(self.example_nif20_normalized, in_nif))
        
    def test_create(self):
        dataset = NIFDataset(uri="http://freme-project.eu")
        
        context = dataset.add_context(
            uri="http://freme-project.eu/doc32",
            mention="Diego Maradona is from Argentina.")
        
        context.add_bean(
           beginIndex=0,
           endIndex=14,
           taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
           score=0.9869992701528016,
           annotator='http://freme-project.eu/tools/freme-ner',
           taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
           taMsClassRef='http://dbpedia.org/ontology/SoccerManager')
        
        context.add_bean(
           beginIndex=23,
           endIndex=32,
           taClassRef=['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
            'http://dbpedia.org/ontology/Place'],
           score=0.9804963628413852,
           annotator='http://freme-project.eu/tools/freme-ner',
           taMsClassRef='http://dbpedia.org/resource/Argentina')

        generated_nif = dataset.dumps(format='turtle')
        self.assertTrue(turtle_equal(self.example_maradona, generated_nif))
        
        parsed_dataset = NIFDataset.loads(generated_nif)
        parsed_context = parsed_dataset.contexts[0]
        
        self.assertEqual(1, len(parsed_dataset.contexts))
        self.assertEqual(context._tuple(), parsed_context._tuple())
        self.assertEqual(dataset, parsed_dataset)
        
        