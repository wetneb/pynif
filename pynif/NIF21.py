from bean import NIFBean
from context import NIFContext
from prefixes import NIFPrefixes


class NIF21():
    def __init__(self):
        self._obj_beans = []
        self._obj_prefixes = NIFPrefixes()

    def context(self, baseURI, beginIndex, endIndex, mention):
        self._obj_context = NIFContext()
        self._obj_context.baseURI = baseURI
        self._obj_context.beginIndex = beginIndex
        self._obj_context.endIndex = endIndex
        self._obj_context.mention = mention

    def bean(self, mention, beginIndex, endIndex, taClassRef, score, annotator, taIdentRef, taMsClassRef):
        bean = NIFBean()
        bean.referenceContext = self._obj_context.referenceContext
        bean.context = self._obj_context.baseURI
        bean.mention = mention
        bean.beginIndex = beginIndex
        bean.endIndex = endIndex
        bean.taClassRef = taClassRef
        bean.score = score
        bean.annotator = annotator
        bean.taIdentRef = taIdentRef
        bean.taMsClassRef = taMsClassRef
        self._obj_beans.append(bean)

    def turtle(self):
        result = ''.join([self._obj_prefixes.turtle, '\n', self._obj_context.turtle, '\n\n'])
        for currentBean in enumerate(self._obj_beans):
            result += currentBean[1].turtle + '\n\n'
        return result
