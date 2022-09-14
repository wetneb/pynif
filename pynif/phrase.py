
from rdflib import URIRef, Literal, Graph
from .prefixes import NIF, XSD, ITSRDF, RDF, RDFS
from .prefixes import NIFPrefixes

from six import binary_type

class NIFPhrase(object):
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
            taIdentRefLabel = None,
            taClassRef = None,
            taMsClassRef = None,
            uri = None,
            is_hash_based_uri = False,
            source = None):
        """
        A phrase can be represented by an OffsetBasedString URI or a
        ContextHashBasedString URI.

        :param: is_hash_based_uri set to True indicates that the :param: uri
        is a ContextHashBasedString, otherwsie is considered as OffsetBasedString.
        :param: taIdentRef is the URI of the concept associated with this phrase
        :param: taIdentRefLabel is its label (rdfs:label)

        ContextHashBasedString is discussed in
        the paper Linked-Data Aware URI Schemes for Referencing Text Fragments
        (https://doi.org/10.1007/978-3-642-33876-2_17) page 4.
        The ContextHashBasedString URI must be provided by the users, it is not
        created automatically.
        """
        self.context = context
        self.annotator = annotator
        self.mention = mention
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.score = score
        self.taIdentRef = taIdentRef
        self.taIdentRefLabel = taIdentRefLabel
        self.taClassRef = taClassRef
        self.taMsClassRef = taMsClassRef
        self.isContextHashBasedString = is_hash_based_uri
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
        Returns the representation of the phrase as RDF triples
        """
        if self.isContextHashBasedString:
            yield (self.uri, RDF.type, NIF.ContextHashBasedString)
        else:
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
            if self.taIdentRefLabel is not None:
                yield (URIRef(self.taIdentRef), RDFS.label, Literal(self.taIdentRefLabel))
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
        Given a RDF graph and a URI which represents a phrase in
        that graph, load the corresponding phrase.
        """
        phrase = cls()
        phrase.original_uri = uri
        for s,p,o in graph.triples((uri, None, None)):
            if p == NIF.anchorOf:
                phrase.mention = o.toPython()
            elif p == NIF.beginIndex:
                phrase.beginIndex = o.toPython()
            elif p == NIF.endIndex:
                phrase.endIndex = o.toPython()
            elif p == NIF.referenceContext:
                phrase.context = o.toPython()
            elif p == ITSRDF.taAnnotatorsRef:
                phrase.annotator = o.toPython()
            elif p == ITSRDF.taConfidence:
                phrase.score = o.toPython()
            elif p == ITSRDF.taIdentRef:
                phrase.taIdentRef = o.toPython()
            elif p == NIF.taMsClassRef:
                phrase.taMsClassRef = o.toPython()
            elif p == ITSRDF.taClassRef:
                if phrase.taClassRef is None:
                    phrase.taClassRef = []
                phrase.taClassRef.append(o.toPython())
            elif p == ITSRDF.taSource:
                phrase.source = o.toPython()
            if o == NIF.ContextHashBasedString :
                phrase.isContextHashBasedString = True

        if phrase.taIdentRef:
            # if there is a concept associated with this phrase, try loading its label
            for o in graph.objects(URIRef(phrase.taIdentRef), RDFS.label):
                phrase.taIdentRefLabel = o.toPython()
                break

        return phrase

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
            return '<NIFPhrase {}-{}: {}>'.format(self.beginIndex, self.endIndex, repr(mention))
        else:
            return '<NIFPhrase (undefined)>'

    def _tuple(self):
        return (self.context,
        self.annotator,
        self.mention,
        self.beginIndex,
        self.endIndex,
        self.score,
        self.taIdentRef,
        self.taIdentRefLabel,
        set(self.taClassRef) if self.taClassRef else set(),
        self.taMsClassRef,
        self.uri,
        self.source)

    def __eq__(self, other):
        return self._tuple() == other._tuple()

    def __hash__(self):
        return hash(self.uri)
