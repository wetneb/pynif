from .context import NIFContext
from rdflib import Graph
from .prefixes import RDF, NIF, NIFPrefixes

class NIFDataset(object):
    """
    A dataset is a set of contexts (snippets of texts that
    are annotated by beans).
    """
    
    def __init__(self):
        self.contexts = []
        
    def triples(self):
        """
        Generates all the triples used to represent this dataset.
        """
        for context in self.contexts:
            for triple in context.triples():
                yield triple
    
    @classmethod
    def load_from_graph(cls, graph):
        """
        Given a RDF graph, load all the contexts it contains
        as one dataset object.
        """
        dataset = NIFDataset()
        for s,p,o in graph.triples((None, RDF.type, NIF.Context)):
            context = NIFContext.load_from_graph(graph, s)
            dataset.contexts.append(context)
        return dataset
    
    @classmethod
    def loads(cls, data, format='turtle'):
        """
        Load a dataset from a string representation of an RDF graph
        """
        g = Graph().parse(format=format,data=data)
        return cls.load_from_graph(g)
    
    def dumps(self, format='turtle'):
        """
        Returns a string representation of the graph in RDF.
        """
        graph = Graph()
        for triple in self.triples():
            graph.add(triple)
        
        graph.namespace_manager = NIFPrefixes().manager
        return graph.serialize(format=format)