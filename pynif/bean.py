
from rdflib import URIRef, Literal, Graph
from .prefixes import NIF, XSD, ITSRDF, RDF
from .prefixes import NIFPrefixes

class NIFBean(object):
    """
    Represents an annotation in a document.
    """
    
    def __init__(self):
        self.context = None
        self.annotator = None
        self.mention = None
        self.beginIndex = None
        self.endIndex = None
        self.score = None
        self.taIdentRef = None
        self.taClassRef = None
        self.referenceContext = None
        self.taMsClassRef = None
        
    @property
    def uri(self):
        return URIRef(self.context + '/#offset_' + str(self.beginIndex) + '_' + str(self.endIndex))

    def triples(self):
        """
        Returns the representation of the bean as RDF triples
        """
        yield (self.uri, RDF.type, NIF.OffsetBasedString)
        yield (self.uri, RDF.type, NIF.Phrase)
        yield (self.uri, NIF.anchorOf, Literal(self.mention))
        yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
        yield (self.uri, NIF.endIndex, Literal(self.endIndex, datatype=XSD.nonNegativeInteger))

        if self.annotator is not None:
            yield (self.uri, ITSRDF.taAnnotatorsRef, URIRef(self.annotator))
        if self.score is not None:
            yield (self.uri, ITSRDF.taConfidence, Literal(str(float(self.score)), datatype=XSD.double, normalize=False))
        if self.taIdentRef is not None:
            yield (self.uri, ITSRDF.taIdentRef, URIRef(self.taIdentRef))
        if self.taMsClassRef is not None:
            yield (self.uri, NIF.taMsClassRef, URIRef(self.taMsClassRef))
        for currentClassRef in self.taClassRef or []:
            yield (self.uri, ITSRDF.taClassRef, URIRef(currentClassRef))
        if self.referenceContext is not None:
            yield (self.uri, NIF.referenceContext, URIRef(self.referenceContext))
        if self.taMsClassRef is not None:
            yield (self.uri, NIF.taMsClassRef, URIRef(self.taMsClassRef))


    @property
    def turtle(self):
        graph = Graph()
        for triple in self.triples():
            graph.add(triple)
        
        graph.namespace_manager = NIFPrefixes().manager
        return graph.serialize(format='turtle')

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        if (self.mention is not None
            and self.beginIndex is not None
            and self.endIndex is not None):
            mention = self.mention
            if len(mention) > 50:
                mention = mention[:50]+'...'
            return '<Bean {}-{}: {}>'.format(self.beginIndex, self.endIndex, repr(mention))
        else:
            return '<Bean (undefined)>'
