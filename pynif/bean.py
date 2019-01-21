
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
    def taMsClassRefStatement(self):
        if self.taMsClassRef is not None:
            return 'nif:taMsClassRef        <' + self.taMsClassRef + '> ;' + '\n\t'
        return ''

    @property
    def annotatorStatement(self):
        if self.annotator is not None:
            return 'itsrdf:taAnnotatorsRef  <' + self.annotator + '> ;' + '\n\t'
        return ''

    @property
    def mentionStatement(self):
        if self.mention is not None:
           return  'nif:anchorOf            "' + self.mention + '" ;\n\t'
        return ''

    @property
    def beginIndexStatement(self):
        if self.beginIndex is not None:
            return 'nif:beginIndex          "' + str(self.beginIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @property
    def endIndexStatement(self):
        if self.endIndex is not None:
            return 'nif:endIndex            "' + str(self.endIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @property
    def scoreStatement(self):
        if self.score is not None:
            return 'itsrdf:taConfidence     "' + str(self.score) + '"^^xsd:double ;\n\t'
        return ''

    @property
    def taIdentRefStatement(self):
        if self.taIdentRef is not None:
            return 'itsrdf:taIdentRef       <' + self.taIdentRef + '> .'
        return ''

    @property
    def referenceContextStatement(self):
        if self.referenceContext is not None:
            return 'nif:referenceContext    <' + self.referenceContext + '> ;' + '\n\t'
        return ''
    
    @property
    def referenceStatement(self):
        return self.taIdentRef + '/#offset_' + str(self.beginIndex) + '_' + str(self.endIndex)

    @property
    def toClassRefStatement(self):
        result = ''
        if self.taClassRef is not None:
            for index, currentClassRef in enumerate(self.taClassRef):
                if (index > 0):
                    result += '<' + currentClassRef + '> , '

        return 'itsrdf:taClassRef       '  + result + ' ;\n\t'

    @property
    def nifBeanProperty(self):
        return 'a                       nif:OffsetBasedString , nif:Phrase ;' + '\n\t'

    @property
    def beanContextStatement(self):
        return '<' + self.context + '/#offset_' + str(self.beginIndex) + '_' + str(self.endIndex) + '>' + '\n\t'

    @property
    def turtle(self):
        return  self.beanContextStatement + \
                self.nifBeanProperty + \
                self.mentionStatement + \
                self.beginIndexStatement + \
                self.endIndexStatement + \
                self.referenceContextStatement + \
                self.taMsClassRefStatement + \
                self.annotatorStatement + \
                self.toClassRefStatement +\
                self.scoreStatement + \
                self.taIdentRefStatement
                
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
