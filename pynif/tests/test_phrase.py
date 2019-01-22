
import unittest
from pynif.phrase import NIFPhrase
from .util import turtle_equal
from rdflib import Graph, URIRef

class NIFPhraseTest(unittest.TestCase):
    
    sample_ttl = """
        @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
        @prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
        @prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
                
        <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_91_102>
            a                       nif:OffsetBasedString , nif:Phrase ;
            nif:anchorOf            "Afghanistan" ;
            nif:beginIndex          "91"^^xsd:nonNegativeInteger ;
            nif:endIndex            "102"^^xsd:nonNegativeInteger ;
            nif:referenceContext    <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1413> ;
            itsrdf:taConfidence     "1"^^xsd:double ;
            itsrdf:taIdentRef       <http://dbpedia.org/resource/Afghanistan> .
        """
    
    def test_to_string_blank(self):
        b = NIFPhrase()
        self.assertEqual("<NIFPhrase (undefined)>", str(b))
        
    def test_to_string(self):
        b = NIFPhrase()
        b.beginIndex = 34
        b.endIndex = 44
        b.mention = "revolution"
        self.assertEqual("""<NIFPhrase 34-44: 'revolution'>""", str(b))
        
    def test_original_uri(self):
        b = NIFPhrase()
        b.original_uri = 'http://example.com/my_annotation'
        self.assertEqual('http://example.com/my_annotation', str(b.uri))
        
    def test_to_turtle(self):
        b = NIFPhrase()
        b.context = 'http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1413'
        b.mention = 'Afghanistan'
        b.beginIndex = 91
        b.endIndex = 102
        b.taClassRef = None
        b.score = 1
        b.taIdentRef = 'http://dbpedia.org/resource/Afghanistan'
        
        self.assertTrue(turtle_equal(self.sample_ttl, b.turtle))
        
    def test_parse(self):
        g = Graph().parse(format='turtle',data=self.sample_ttl)
        uri = URIRef('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_91_102')
        phrase = NIFPhrase.load_from_graph(g, uri)
        
        self.assertEqual('Afghanistan', phrase.mention)
        self.assertEqual(91, phrase.beginIndex)
        self.assertEqual(102, phrase.endIndex)
        self.assertEqual(1., phrase.score)
        self.assertEqual('http://dbpedia.org/resource/Afghanistan', phrase.taIdentRef)
        