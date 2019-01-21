from .bean import NIFBean

class NIFContext(object):

    def __init__(self):
        self.baseURI = None
        self.beginIndex = None
        self.endIndex = None
        self.mention = None
        self.beans = []

    def addBean(self, beginIndex=None, endIndex=None):
        bean = NIFBean()
        bean.context = self.baseURI
        bean.referenceContext = self.referenceContext
        bean.beginIndex = beginIndex
        bean.endIndex = endIndex
        if beginIndex is not None and endIndex is not None:
            bean.mention = self.mention[beginIndex:endIndex]
        self.beans.append(bean)
        return bean

    @property
    def beginIndexStatement(self):
        if self.beginIndex is not None:
            return 'nif:beginIndex  "' + str(self.beginIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @property
    def endIndexStatement(self):
        if self.endIndex is not None:
            return 'nif:endIndex    "' + str(self.endIndex) + '"^^xsd:nonNegativeInteger ;\n\t'
        return ''

    @property
    def referenceContext(self):
        return  self.baseURI + '/#offset_' + str(self.beginIndex) + '_' + str(self.endIndex)

    @property
    def nifContextProperty(self):
        return 'a                       nif:OffsetBasedString , nif:Context ;' + '\n\t'

    @property
    def turtle(self):
        initial_turtle = '<' + self.referenceContext + '>\n\t' + \
               self.nifContextProperty + \
               self.beginIndexStatement + \
               self.endIndexStatement + \
               'nif:isString    "' + self.mention.replace('"', '\\"') + '" .\n\n<' + self.baseURI+ '/#collection>' +\
               '\n\ta               nif:ContextCollection ;' + \
               '\n\tnif:hasContext\t<' + self.referenceContext +'>\n\t' +\
               '<http://purl.org/dc/terms/conformsTo>\n\t\t<http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1> .\n\n'
               
        beans_turtle = '\n\n'.join(bean.turtle for bean in self.beans)
        return initial_turtle + beans_turtle
    
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
    
