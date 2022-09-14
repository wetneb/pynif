from rdflib.namespace import Namespace, NamespaceManager
import rdflib.namespace
from rdflib.graph import Graph

XSD = rdflib.namespace.XSD
RDF = rdflib.namespace.RDF
RDFS = rdflib.namespace.RDFS
DCTERMS = rdflib.namespace.DCTERMS
ITSRDF = Namespace('http://www.w3.org/2005/11/its/rdf#')
NIF = Namespace('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#')

nif_ontology_uri = 'http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1'

class NIFPrefixes:

    def __init__(self):
        self.manager = NamespaceManager(Graph())
        self.manager.bind("xsd", XSD)
        self.manager.bind("itsrdf", ITSRDF)
        self.manager.bind("nif", NIF)

        self._XSD = '@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .\n'
        self._ITSRDF = '@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .\n'
        self._NIF = '@prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .\n'

    @property
    def turtle(self):
        return self._XSD + self._ITSRDF + self._NIF
