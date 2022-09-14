from rdflib import URIRef, Literal, Graph
from .phrase import NIFPhrase
from .prefixes import NIF, XSD, ITSRDF, RDF, DCTERMS, nif_ontology_uri
from .prefixes import NIFPrefixes

from six import binary_type


class NIFContext(object):
    """
    A context is a string which can be annotated by phrases.
    """

    def __init__(self,
                 beginIndex=None,
                 endIndex=None,
                 mention=None,
                 sourceUrl=None,
                 uri=None,
                 is_hash_based_uri = False):
        """
        A context can be represented by an OffsetBasedString URI or a
        ContextHashBasedString URI.

        :pram: is_hash_based_uri set to True indicates that the :param: uri
        is a ContextHashBasedString, otherwsie is considered as OffsetBasedString.

        ContextHashBasedString is discussed in
        the paper Linked-Data Aware URI Schemes for Referencing Text Fragments
        (https://doi.org/10.1007/978-3-642-33876-2_17) page 4.
        The ContextHashBasedString URI must be provided by the users, it is not
        created automatically.
        """
        self.isContextHashBasedString = is_hash_based_uri
        self.original_uri = uri
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.mention = mention
        if mention is not None and beginIndex is None:
            self.beginIndex = 0
        if mention is not None and endIndex is None:
            self.endIndex = len(mention)
        self.sourceUrl = sourceUrl
        self.phrases = []

    def add_phrase(self,
            beginIndex=None,
            endIndex=None,
            annotator = None,
            score = None,
            taIdentRef = None,
            taIdentRefLabel = None,
            taClassRef = None,
            taMsClassRef = None,
            uri = None,
            source = None,
            is_hash_based_uri = False):
        """
        Creates a new annotation in this document.

        :returns: the new {@class NIFPhrase}
        """
        phrase = NIFPhrase(context = self.original_uri,
                beginIndex = beginIndex,
                endIndex = endIndex,
                annotator = annotator,
                score = score,
                taIdentRef = taIdentRef,
                taIdentRefLabel = taIdentRefLabel,
                taClassRef = taClassRef,
                taMsClassRef = taMsClassRef,
                uri = uri,
                source = source,
                is_hash_based_uri= is_hash_based_uri)
        if beginIndex is not None and endIndex is not None:
            phrase.mention = self.mention[beginIndex:endIndex]
        self.phrases.append(phrase)
        return phrase

    @property
    def uri(self):
        return URIRef(self.original_uri)

    def triples(self):
        """
        Returns the representation of the context as RDF triples
        """
        if self.isContextHashBasedString:
            yield (self.uri, RDF.type, NIF.ContextHashBasedString)
        else:
            yield (self.uri, RDF.type, NIF.OffsetBasedString)
        yield (self.uri, RDF.type, NIF.Context)
        yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
        yield (self.uri, NIF.endIndex, Literal(self.endIndex, datatype=XSD.nonNegativeInteger))
        yield (self.uri, NIF.isString, Literal(self.mention))
        if self.sourceUrl is not None:
            yield (self.uri, NIF.sourceUrl, URIRef(self.sourceUrl))

        for phrase in self.phrases:
            for triple in phrase.triples():
                yield triple

    @classmethod
    def load_from_graph(cls, graph, uri):
        """
        Given a RDF graph and a URI which represents a context in
        that graph, load the corresponding context and its child phrases.
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
            if o == NIF.ContextHashBasedString :
                context.isContextHashBasedString = True

        # Load child phrases
        for s,p,o in graph.triples((None, NIF.referenceContext, uri)):
             phrase = NIFPhrase.load_from_graph(graph, s)
             context.phrases.append(phrase)

        return context

    @property
    def turtle(self):
        graph = Graph()
        for triple in self.triples():
            graph.add(triple)

        graph.namespace_manager = NIFPrefixes().manager
        out = graph.serialize(format='turtle')

        # workaround for https://github.com/RDFLib/rdflib/issues/884
        if isinstance(out, binary_type):
            out = out.decode('utf-8')
        return out

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
            set(self.phrases))

    def __eq__(self, other):
        return self._tuple() == other._tuple()

    def __hash__(self):
        return hash(self.uri)

