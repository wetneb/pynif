
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

    sample_ttl_with_label = """
        @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
        @prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
        @prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_91_102>
            a                       nif:OffsetBasedString , nif:Phrase ;
            nif:anchorOf            "Afghanistan" ;
            nif:beginIndex          "91"^^xsd:nonNegativeInteger ;
            nif:endIndex            "102"^^xsd:nonNegativeInteger ;
            nif:referenceContext    <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1413> ;
            itsrdf:taConfidence     "1"^^xsd:double ;
            itsrdf:taIdentRef       <http://dbpedia.org/resource/Afghanistan> .

        <http://dbpedia.org/resource/Afghanistan> rdfs:label "Afghanistan".
        """

    example_text = "    Primary Navigation Secondary Navigation Search: Nearly 60 militants killed in southern Afghanistan Tue Oct 7, 9:14 AM ET KABUL (Reuters) - U.S.-led coalition and Afghan security forces killed nearly 60 militants during separate clashes in southern Afghanistan, the U.S. military and a police official said Tuesday. Violence has surged in the war-torn country with some 3,800 people, a third of them civilians, killed as a result of the conflict by the end of July this year, according to the United Nations. U.S.-led coalition and Afghan security forces killed 43 militants during heavy fighting in Qalat district of southern Zabul province Sunday, the U.S. military said in a statement Tuesday. \"ANSF (Afghan National Security Forces ) and coalition forces on a patrol received heavy weapons, machine gun and sniper fire from militants in multiple locations,\" the U.S. military said in a statement. The combined forces responded with small arms fire , rocket propelled grenades and close air support , killing the militants, it said. No Afghan or U.S.-led troops were killed or wounded during incident, it said. In a separate incident, Afghan and international troops killed 16 Taliban insurgents and wounded six more during a gun battle in Nad Ali district of southern Helmand province on Monday, provincial police chief Asadullah Sherzad told Reuters. (Writing by Jonathon Burch; Editing by Bill Tarrant)"
    example_turtle_ContextHashBasedString = """
        @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
        @prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
        @prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .

        <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_1400_1411_9f215ab78483a223463f9726ee0e92c0_%20%20%20%20Primary%20Navigati>
            a                       nif:ContextHashBasedString , nif:Phrase ;
            nif:anchorOf            "Afghanistan" ;
            nif:beginIndex          "91"^^xsd:nonNegativeInteger ;
            nif:endIndex            "102"^^xsd:nonNegativeInteger ;
            nif:referenceContext    <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_0_1411_6218664a3a8c7bed58460e329ddc6904_%20%20%20%20Primary%20Navigati> ;
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

    def test_to_turtle_with_label(self):
        b = NIFPhrase()
        b.context = 'http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1413'
        b.mention = 'Afghanistan'
        b.beginIndex = 91
        b.endIndex = 102
        b.taClassRef = None
        b.score = 1
        b.taIdentRef = 'http://dbpedia.org/resource/Afghanistan'
        b.taIdentRefLabel = 'Afghanistan'

        self.assertTrue(turtle_equal(b.turtle, self.sample_ttl_with_label))

    def test_parse(self):
        g = Graph().parse(format='turtle',data=self.sample_ttl)
        uri = URIRef('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_91_102')
        phrase = NIFPhrase.load_from_graph(g, uri)

        self.assertEqual('Afghanistan', phrase.mention)
        self.assertEqual(91, phrase.beginIndex)
        self.assertEqual(102, phrase.endIndex)
        self.assertEqual(1., phrase.score)
        self.assertEqual('http://dbpedia.org/resource/Afghanistan', phrase.taIdentRef)

    def test_parse_with_label(self):
        g = Graph().parse(format='turtle',data=self.sample_ttl_with_label)
        uri = URIRef('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_91_102')
        phrase = NIFPhrase.load_from_graph(g, uri)

        self.assertEqual('Afghanistan', phrase.mention)
        self.assertEqual(91, phrase.beginIndex)
        self.assertEqual(102, phrase.endIndex)
        self.assertEqual(1., phrase.score)
        self.assertEqual('http://dbpedia.org/resource/Afghanistan', phrase.taIdentRef)
        self.assertEqual('Afghanistan', phrase.taIdentRefLabel)

    def test_create_ContextHashBasedString_phrase(self):
        phrase = NIFPhrase(
            uri='http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_1400_1411_9f215ab78483a223463f9726ee0e92c0_%20%20%20%20Primary%20Navigati',
            is_hash_based_uri = True,
            context = "http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_0_1411_6218664a3a8c7bed58460e329ddc6904_%20%20%20%20Primary%20Navigati",
            beginIndex=91,
            endIndex=102,
            mention= self.example_text[91:102],
            score=1.,
            taIdentRef="http://dbpedia.org/resource/Afghanistan")

        self.assertEqual('Afghanistan', phrase.mention)
        self.assertEqual(91, phrase.beginIndex)
        self.assertEqual(102, phrase.endIndex)
        self.assertEqual(1., phrase.score)
        self.assertTrue(turtle_equal(self.example_turtle_ContextHashBasedString, phrase.turtle))

if __name__ == '__main__':
    unittest.main()
