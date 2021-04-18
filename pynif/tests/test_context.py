
import unittest
from pynif.context import NIFContext
from .util import turtle_equal
from rdflib import Graph, URIRef

class NIFContextTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.example_text = "    Primary Navigation Secondary Navigation Search: Nearly 60 militants killed in southern Afghanistan Tue Oct 7, 9:14 AM ET KABUL (Reuters) - U.S.-led coalition and Afghan security forces killed nearly 60 militants during separate clashes in southern Afghanistan, the U.S. military and a police official said Tuesday. Violence has surged in the war-torn country with some 3,800 people, a third of them civilians, killed as a result of the conflict by the end of July this year, according to the United Nations. U.S.-led coalition and Afghan security forces killed 43 militants during heavy fighting in Qalat district of southern Zabul province Sunday, the U.S. military said in a statement Tuesday. \"ANSF (Afghan National Security Forces ) and coalition forces on a patrol received heavy weapons, machine gun and sniper fire from militants in multiple locations,\" the U.S. military said in a statement. The combined forces responded with small arms fire , rocket propelled grenades and close air support , killing the militants, it said. No Afghan or U.S.-led troops were killed or wounded during incident, it said. In a separate incident, Afghan and international troops killed 16 Taliban insurgents and wounded six more during a gun battle in Nad Ali district of southern Helmand province on Monday, provincial police chief Asadullah Sherzad told Reuters. (Writing by Jonathon Burch; Editing by Bill Tarrant)"
        cls.example_turtle = """
            @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
            @prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
            @prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
                    
            <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1411>
                a                       nif:OffsetBasedString , nif:Context ;
                nif:beginIndex  "0"^^xsd:nonNegativeInteger ;
                nif:endIndex    "{}"^^xsd:nonNegativeInteger ;
                nif:isString    "{}" .
        """.format(len(cls.example_text), cls.example_text.replace('"', '\\"'))
    
    def test_to_string_undefined(self):
        c = NIFContext()
        self.assertEqual("<NIFContext (undefined)>", str(c))
        
    def test_to_string(self):
        c = NIFContext()
        c.baseURI = 'http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/'
        c.beginIndex = 0
        c.mention = "    Primary Navigation Secondary Navigation Search: Nearly 60 militants killed"
        c.endIndex = len(c.mention)
        self.assertEqual("<NIFContext 0-78: '    Primary Navigation Secondary Navigation Search...'>", str(c))
        
    def test_original_uri(self):
        b = NIFContext()
        b.original_uri = 'http://example.com/my_annotation'
        self.assertEqual('http://example.com/my_annotation', str(b.uri))
        
    def test_add_phrase(self):
        c = NIFContext(uri = 'http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0',
                       mention = self.example_text)
        
        b = c.add_phrase(91, 102)
        self.assertEqual(91, b.beginIndex)
        self.assertEqual(102, b.endIndex)
        self.assertEqual("Afghanistan", b.mention)
        self.assertEqual("http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0", b.context)
        
    def test_turtle(self):
        c = NIFContext(
            uri='http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1411',
            mention=self.example_text)

        self.assertTrue(turtle_equal(self.example_turtle, c.turtle))
        
    def test_load_from_graph(self):
        g = Graph().parse(format='turtle',data=self.example_turtle)
        uri = URIRef('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc/yn_08Oct08_file_0/#offset_0_1411')
        context = NIFContext.load_from_graph(g, uri)
        
        self.assertEqual(self.example_text, context.mention)
        self.assertEqual(0, context.beginIndex)
        self.assertEqual(len(self.example_text), context.endIndex)
    
    def test_create_ContextHashBasedString_context(self):
        c = NIFContext(
            uri='http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_0_1411_6218664a3a8c7bed58460e329ddc6904_%20%20%20%20Primary%20Navigati',
            mention=self.example_text,
            is_hash_based_uri=True)
        self.example_turtle_ContextHashBasedString = """
            @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
            @prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
            @prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
                    
            <http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_0_1411_6218664a3a8c7bed58460e329ddc6904_%20%20%20%20Primary%20Navigati>
                a                       nif:ContextHashBasedString , nif:Context ;
                nif:beginIndex  "0"^^xsd:nonNegativeInteger ;
                nif:endIndex    "{}"^^xsd:nonNegativeInteger ;
                nif:isString    "{}" .
        """.format(len(self.example_text), self.example_text.replace('"', '\\"'))
        self.assertTrue(turtle_equal(self.example_turtle_ContextHashBasedString, c.turtle))

    def test_create_populated_ContextHashBasedString(self):
        context = NIFContext(
                uri='http://freme-project.eu#hash_0_33_cf35b7e267d05b7ca8aba0651641050b_Diego%20Maradona%20is%20fr',
                mention="Diego Maradona is from Argentina.",
                is_hash_based_uri = True)
        context.add_phrase(
                uri='http://freme-project.eu#hash_19_33_158118325b076b079d3969108872d855_Diego%20Maradona%20is%20fr',
                is_hash_based_uri = True,
                beginIndex=0,
                endIndex=14,
                score=0.9869992701528016,
                taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
                annotator='http://freme-project.eu/tools/freme-ner',
                taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
                taMsClassRef='http://dbpedia.org/ontology/SoccerManager')
        self.example_turtle_ContextHashBasedString = """
            @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
            @prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
            @prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
                
            <http://freme-project.eu#hash_0_33_cf35b7e267d05b7ca8aba0651641050b_Diego%20Maradona%20is%20fr>
                a nif:ContextHashBasedString , nif:Context ;
                nif:beginIndex  "0"^^xsd:nonNegativeInteger ;
                nif:endIndex    "33"^^xsd:nonNegativeInteger ;
                nif:isString    "Diego Maradona is from Argentina." .

            <http://freme-project.eu#hash_19_33_158118325b076b079d3969108872d855_Diego%20Maradona%20is%20fr>
                a nif:ContextHashBasedString, nif:Phrase ;
                nif:anchorOf "Diego Maradona" ;
                nif:beginIndex "0"^^xsd:nonNegativeInteger ;
                nif:endIndex "14"^^xsd:nonNegativeInteger ;
                nif:referenceContext <http://freme-project.eu#hash_0_33_cf35b7e267d05b7ca8aba0651641050b_Diego%20Maradona%20is%20fr> ;
                nif:taMsClassRef <http://dbpedia.org/ontology/SoccerManager> ;
                itsrdf:taAnnotatorsRef <http://freme-project.eu/tools/freme-ner> ;
                itsrdf:taClassRef <http://dbpedia.org/ontology/Person>, <http://dbpedia.org/ontology/SportsManager>, <http://nerd.eurecom.fr/ontology#Person> ;
                itsrdf:taConfidence 9.869993e-01 ;
                itsrdf:taIdentRef <http://dbpedia.org/resource/Diego_Maradona> .
        """
        self.assertTrue(turtle_equal(self.example_turtle_ContextHashBasedString, context.turtle))




if __name__ == '__main__':
    unittest.main()