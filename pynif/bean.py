
from rdflib import URIRef, Literal, Graph
from .prefixes import NIF, XSD, ITSRDF, RDF
from .prefixes import NIFPrefixes

class NIFBean(object):
    """
    Represents an annotation in a document.
    """
    
    def __init__(self,
            context = None,
            annotator = None,
            mention = None,
            beginIndex = None,
            endIndex = None,
            score = None,
            taIdentRef = None,
            taClassRef = None,
            taMsClassRef = None,
            uri = None,
            source = None):
        self.context = context
        self.annotator = annotator
        self.mention = mention
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.score = score
        self.taIdentRef = taIdentRef
        self.taClassRef = taClassRef
        self.taMsClassRef = taMsClassRef
        self.original_uri = uri
        self.source = source
        
    @property
    def uri(self):
        return URIRef(self.original_uri or self.generated_uri)
        
    @property
    def generated_uri(self):
        return self.context.split('#')[0] + '#offset_' + str(self.beginIndex) + '_' + str(self.endIndex)

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
        if self.context is not None:
            yield (self.uri, NIF.referenceContext, URIRef(self.context))
        if self.taMsClassRef is not None:
            yield (self.uri, NIF.taMsClassRef, URIRef(self.taMsClassRef))
        if self.source is not None:
            yield (self.uri, ITSRDF.taSource, Literal(self.source, datatype=XSD.string))
            
    @classmethod
    def load_from_graph(cls, graph, uri):
        """
        Given a RDF graph and a URI which represents a bean in
        that graph, load the corresponding bean.
        """
        bean = cls()
        bean.original_uri = uri
        for s,p,o in graph.triples((uri, None, None)):
            if p == NIF.anchorOf:
                bean.mention = o.toPython()
            elif p == NIF.beginIndex:
                bean.beginIndex = o.toPython()
            elif p == NIF.endIndex:
                bean.endIndex = o.toPython()
            elif p == NIF.referenceContext:
                bean.context = o.toPython()
            elif p == ITSRDF.taAnnotatorsRef:
                bean.annotator = o.toPython()
            elif p == ITSRDF.taConfidence:
                bean.score = o.toPython()
            elif p == ITSRDF.taIdentRef:
                bean.taIdentRef = o.toPython()
            elif p == NIF.taMsClassRef:
                bean.taMsClassRef = o.toPython()
            elif p == ITSRDF.taClassRef:
                if bean.taClassRef is None:
                    bean.taClassRef = []
                bean.taClassRef.append(o.toPython())
            elif p == ITSRDF.taSource:
                bean.source = o.toPython()
        return bean

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
        
    def _tuple(self):
        return (self.context,
        self.annotator,
        self.mention,
        self.beginIndex,
        self.endIndex,
        self.score,
        self.taIdentRef,
        self.taClassRef,
        self.taMsClassRef,
        self.original_uri,
        self.source)
        
    def __eq__(self, other):
        return self._tuple() == other._tuple()
    
    def __hash__(self):
        return hash(self.uri)
