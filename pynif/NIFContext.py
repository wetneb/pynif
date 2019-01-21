class NIFContext(object):

    def __init__(self):
        self._baseURI = None
        self._beginIndex = None
        self._endIndex = None
        self._mention = None

    @property
    def baseURI(self):
        return self._baseURI

    @baseURI.setter
    def baseURI(self, value):
        self._baseURI = value

    @baseURI.deleter
    def baseURI(self):
        del self._baseURI

    @property
    def beginIndex(self):
        if self._beginIndex is not None:
            return 'nif:beginIndex  "' + str(self._beginIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @beginIndex.setter
    def beginIndex(self, value):
        self._beginIndex = value

    @beginIndex.deleter
    def beginIndex(self):
        del self._beginIndex

    @property
    def endIndex(self):
        if self._endIndex is not None:
            return 'nif:endIndex    "' + str(self._endIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @endIndex.setter
    def endIndex(self, value):
        self._endIndex = value


    @endIndex.deleter
    def endIndex(self):
        del self._endIndex

    @property
    def mention(self):
        return self._mention

    @mention.setter
    def mention(self, value):
        self._mention = value

    @mention.deleter
    def mention(self):
        del self._mention

    @property
    def referenceContext(self):
        return  self._baseURI + '/#offset_' + str(self._beginIndex) + '_' + str(self._endIndex)

    @property
    def nifContextProperty(self):
        return 'a                       nif:OffsetBasedString , nif:Context ;' + '\n\t'

    @property
    def turtle(self):
        return '<' + self.referenceContext + '>\n\t' + \
               self.nifContextProperty + \
               self.beginIndex + \
               self.endIndex + \
               'nif:isString    "' + self._mention + '" . \n\n<' + self._baseURI+ '/#collection>' +\
               '\n\ta               nif:ContextCollection ;' + \
               '\n\tnif:hasContext\t<' + self.referenceContext +'>\n\t' +\
               '<http://purl.org/dc/terms/conformsTo>\n\t\t<http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1> .\t\t'