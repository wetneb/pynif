from .context import NIFContext
from rdflib import Graph, URIRef
from .prefixes import RDF, NIF, DCTERMS, NIFPrefixes, nif_ontology_uri

class NIFDataset(object):
    """
    A dataset (or context collection) is a set of contexts (snippets of texts that
    are annotated by beans).
    """
    
    def __init__(self, uri=None):
        self.contexts = []
        self.original_uri = uri
        
    @property
    def uri(self):
        return URIRef(self.original_uri)
        
    def add_context(self, uri, mention, beginIndex=None, endIndex=None):
        """
        Adds a context to the dataset. Returns the context.
        """
        c = NIFContext(uri=uri, mention=mention, beginIndex=beginIndex, endIndex=endIndex)
        self.contexts.append(c)
        return c
        
    def triples(self):
        """
        Generates all the triples used to represent this dataset.
        """
        if self.original_uri is not None:
            yield (self.uri, RDF.type, NIF.ContextCollection)
            yield (self.uri, DCTERMS.conformsTo, URIRef(nif_ontology_uri))
            for context in self.contexts:
                yield (self.uri, NIF.hasContext, context.uri)
        
        for context in self.contexts:
            for triple in context.triples():
                yield triple
    
    @classmethod
    def load_from_graph(cls, graph, uri=None):
        """
        Given a RDF graph, load all the contexts it contains
        as one dataset object.
        
        If no URI is provided, all the nif:Context in the graph
        will be loaded (compatibility with NIF 2.0).
        """
        uri_ref = None
        if uri is not None:
            uri_ref = uri.toPython()
            
        dataset = NIFDataset(uri=uri_ref)
        # Load collection
        if uri is not None:
            context_uris = [o for s,p,o in graph.triples((uri, NIF.hasContext, None))]
        else:
            context_uris = [s for s,p,o in graph.triples((None, RDF.type, NIF.Context))]
        
        for u in context_uris:
            context = NIFContext.load_from_graph(graph, u)
            dataset.contexts.append(context)

        return dataset
    
    @classmethod
    def loads(cls, data, format='turtle', uri=None):
        """
        Load a dataset from a string representation of an RDF graph.
        
        If no URI for the dataset is provided, we scan the graph to find
        the first ContextCollection in it. In there isn't any, the dataset
        will load all available nif:Context in the graph.
        """
        g = Graph().parse(format=format,data=data)
        if uri is None:
            for s,p,o in g.triples((None, RDF.type, NIF.ContextCollection)):
                uri = s
                break
        return cls.load_from_graph(g, uri)
    
    def dumps(self, format='turtle'):
        """
        Returns a string representation of the graph in RDF.
        """
        graph = Graph()
        for triple in self.triples():
            graph.add(triple)
        
        graph.namespace_manager = NIFPrefixes().manager
        return graph.serialize(format=format)