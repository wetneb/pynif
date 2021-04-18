import unittest
import os
from pynif.collection import NIFCollection
from .util import turtle_equal

class NIFCollectionTest(unittest.TestCase):

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
        cls.testdir = testdir

    def test_serialize_nif21(self):
        collection = NIFCollection.loads(self.example_nif21)

        self.assertEqual(1, len(collection.contexts))
        context = collection.contexts[0]
        self.assertEqual(3, len(context.phrases))

        in_nif = collection.dumps()

        self.assertTrue(turtle_equal(self.example_nif21, in_nif))

    def test_serialize_nif20(self):
        collection = NIFCollection.loads(self.example_nif20)

        self.assertEqual(1, len(collection.contexts))
        context = collection.contexts[0]
        self.assertEqual(3, len(context.phrases))

        in_nif = collection.dumps()

        self.assertTrue(turtle_equal(self.example_nif20_normalized, in_nif))

    def test_file_helpers(self):
        c = NIFCollection.load(os.path.join(self.testdir, 'data/reuters-nif21.ttl'))
        c2 = NIFCollection.loads(self.example_nif21)
        self.assertEqual(c, c2)

    def test_create(self):
        collection = NIFCollection(uri="http://freme-project.eu")

        context = collection.add_context(
            uri="http://freme-project.eu/doc32",
            mention="Diego Maradona is from Argentina.")

        context.add_phrase(
           beginIndex=0,
           endIndex=14,
           taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
           score=0.9869,
           annotator='http://freme-project.eu/tools/freme-ner',
           taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
           taMsClassRef='http://dbpedia.org/ontology/SoccerManager')

        context.add_phrase(
           beginIndex=23,
           endIndex=32,
           taClassRef=['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
            'http://dbpedia.org/ontology/Place'],
           score=0.9804,
           annotator='http://freme-project.eu/tools/freme-ner',
           taMsClassRef='http://dbpedia.org/resource/Argentina')

        generated_nif = collection.dumps(format='turtle')
        self.assertTrue(turtle_equal(self.example_maradona, generated_nif))

        parsed_collection = NIFCollection.loads(generated_nif)
        parsed_context = parsed_collection.contexts[0]

        self.assertEqual(1, len(parsed_collection.contexts))
        self.assertEqual(collection, parsed_collection)


if __name__ == '__main__':
    unittest.main()