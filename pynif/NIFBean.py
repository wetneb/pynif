class NIFBean(object):
    def __init__(self):
        self._context = None
        self._annotator = None
        self._mention = None
        self._beginIndex = None
        self._endIndex = None
        self._score = None
        self._taIdentRef = None
        self._taClassRef = None
        self._referenceContext = None
        self._taMsClassRef = None

    @property
    def taMsClassRef(self):
        if self._taMsClassRef is not None:
            return 'nif:taMsClassRef        <' + self._taMsClassRef + '> ;' + '\n\t'
        return ''

    @taMsClassRef.setter
    def taMsClassRef(self, value):
        self._taMsClassRef = value

    @taMsClassRef.deleter
    def taMsClassRef(self):
        del self._taMsClassRef

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @context.deleter
    def context(self):
        del self._context

    @property
    def annotator(self):
        if self._annotator is not None:
            return 'itsrdf:taAnnotatorsRef  <' + self._annotator + '> ;' + '\n\t'
        return ''

    @annotator.setter
    def annotator(self, value):
        self._annotator = value

    @annotator.deleter
    def annotator(self):
        del self._annotator

    @property
    def mention(self):
        if self._mention is not None:
           return  'nif:anchorOf            "' + self._mention + '" ;\n\t'
        return ''

    @mention.setter
    def mention(self, value):
        self._mention = value

    @mention.deleter
    def mention(self):
        del self._mention

    @property
    def beginIndex(self):
        if self._beginIndex is not None:
            return 'nif:beginIndex          "' + str(self._beginIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
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
            return 'nif:endIndex            "' + str(self._endIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @endIndex.setter
    def endIndex(self, value):
        self._endIndex = value

    @endIndex.deleter
    def endIndex(self):
        del self._endIndex

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, value):
        self._types = value

    @types.deleter
    def types(self):
        del self._types

    @property
    def score(self):
        if self._score is not None:
            return 'itsrdf:taConfidence     "' + str(self._score) + '^^xsd:double ;\n\t'
        return ''

    @score.setter
    def score(self, value):
        self._score = value

    @score.deleter
    def score(self):
        del self._score

    @property
    def taIdentRef(self):
        if self._taIdentRef is not None:
            return 'itsrdf:taIdentRef       <' + self._taIdentRef + '> .'
        return ''

    @taIdentRef.setter
    def taIdentRef(self, value):
        self._taIdentRef = value

    @taIdentRef.deleter
    def taIdentRef(self):
        del self._taIdentRef

    @property
    def taClassRef(self):
        return self._taClassRef

    @taClassRef.setter
    def taClassRef(self, value):
        self._taClassRef = value

    @taClassRef.deleter
    def taClassRef(self):
        del self._taClassRef

    @property
    def referenceContext(self):
        if self._referenceContext is not None:
            return 'nif:referenceContext    <' + self._referenceContext + '> ;' + '\n\t'
        return ''

    @referenceContext.setter
    def referenceContext(self, value):
        self._referenceContext = value

    @referenceContext.deleter
    def referenceContext(self):
        del self._referenceContext

    @property
    def reference(self):
        return self._taIdentRef + '/#offset_' + str(self._beginIndex) + '_' + str(self._endIndex)

    @property
    def toClassRef(self):
        result = ''
        if self._taClassRef is not None:
            for index, currentClassRef in enumerate(self._taClassRef):
                if (index > 0):
                    result += '<' + currentClassRef + '> , '

        return 'itsrdf:taClassRef       '  + result + ' ;\n\t'

    @property
    def nifBeanProperty(self):
        return 'a                       nif:OffsetBasedString , nif:Phrase ;' + '\n\t'

    @property
    def beanContext(self):
        return '<' + self._context + '/#offset_' + str(self._beginIndex) + '_' + str(self._endIndex) + '>' + '\n\t'

    @property
    def turtle(self):
        return  self.beanContext + \
                self.nifBeanProperty + \
                self.mention + \
                self.beginIndex + \
                self.endIndex + \
                self.referenceContext + \
                self.taMsClassRef + \
                self.annotator + \
                self.toClassRef +\
                self.score + \
                self.taIdentRef
