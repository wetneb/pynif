from rdflib import URIRef, Literal, Graph
from .bean import NIFBean
from .prefixes import NIF, XSD, ITSRDF, RDF, DCTERMS, nif_ontology_uri
from .prefixes import NIFPrefixes

class NIFContext(object):
    """
    A context is a string which can be annotated by beans.
    """

    def __init__(self,
                 beginIndex=None,
                 endIndex=None,
                 mention=None,
                 sourceUrl=None,
                 uri=None):
        self.original_uri = uri
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.mention = mention
        if mention is not None and beginIndex is None:
            self.beginIndex = 0
        if mention is not None and endIndex is None:
            self.endIndex = len(mention)
        self.sourceUrl = sourceUrl
        self.beans = []

    def add_bean(self,
            beginIndex=None,
            endIndex=None,    
            annotator = None,
            score = None,
            taIdentRef = None,
            taClassRef = None,
            taMsClassRef = None,
            uri = None,
            source = None):
        """
        Creates a new annotation in this document.
        
        :returns: the new {@class NIFBean}
        """
        bean = NIFBean(context = self.original_uri,
                beginIndex = beginIndex,
                endIndex = endIndex,
                annotator = annotator,
                score = score,
                taIdentRef = taIdentRef,
                taClassRef = taClassRef,
                taMsClassRef = taMsClassRef,
                uri = uri,
                source = source)
        if beginIndex is not None and endIndex is not None:
            bean.mention = self.mention[beginIndex:endIndex]
        self.beans.append(bean)
        return bean
    
    @property
    def uri(self):
        return URIRef(self.original_uri)
    
    def triples(self):
        """
        Returns the representation of the context as RDF triples
        """
        yield (self.uri, RDF.type, NIF.OffsetBasedString)
        yield (self.uri, RDF.type, NIF.Context)
        yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
        yield (self.uri, NIF.endIndex, Literal(self.endIndex, datatype=XSD.nonNegativeInteger))
        yield (self.uri, NIF.isString, Literal(self.mention))
        if self.sourceUrl is not None:
            yield (self.uri, NIF.sourceUrl, URIRef(self.sourceUrl))
               
        for bean in self.beans:
            for triple in bean.triples():
                yield triple
        
    @classmethod
    def load_from_graph(cls, graph, uri):
        """
        Given a RDF graph and a URI which represents a context in
        that graph, load the corresponding context and its child beans.
        """
        context = cls()
        context.original_uri = uri.toPython()
        # Load core data
        for s,p,o in graph.triples((uri, None, None)):
            if p == NIF.isString:
                context.mention = o.toPython()
            elif p == NIF.beginIndex:
                context.beginIndex = o.toPython()
            elif p == NIF.endIndex:
                context.endIndex = o.toPython()
            elif p == NIF.sourceUrl:
                context.sourceUrl = o.toPython()
            
        # Load child beans
        for s,p,o in graph.triples((None, NIF.referenceContext, uri)):
             bean = NIFBean.load_from_graph(graph, s)
             context.beans.append(bean)
             
        return context

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
            return '<NIFContext {}-{}: {}>'.format(self.beginIndex, self.endIndex, repr(mention))
        else:
            return '<NIFContext (undefined)>'
        
    def _tuple(self):
        return (self.uri,
            self.beginIndex,
            self.endIndex,
            self.mention,
            self.sourceUrl,
            set(self.beans))
    
    def __eq__(self, other):
        return self._tuple() == other._tuple()
    
    def __hash__(self):
        return hash(self.uri)
    
