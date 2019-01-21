from bean import NIFBean
from context import NIFContext
from prefixes import NIFPrefixes


class NIF21():
    def __init__(self):
        self._obj_contextes = []
        self._obj_prefixes = NIFPrefixes()

    def context(self, baseURI, beginIndex, endIndex, mention):
        self._obj_context = NIFContext()
        self._obj_context.baseURI = baseURI
        self._obj_context.beginIndex = beginIndex
        self._obj_context.endIndex = endIndex
        self._obj_context.mention = mention
        self._obj_contextes.append(self._obj_context)

    def bean(self, mention, beginIndex, endIndex, taClassRef, score, annotator, taIdentRef, taMsClassRef):
        bean = self._obj_context.addBean(beginIndex, endIndex)
        bean.taClassRef = taClassRef
        bean.score = score
        bean.annotator = annotator
        bean.taIdentRef = taIdentRef
        bean.taMsClassRef = taMsClassRef

    def turtle(self):
        return self._obj_prefixes.turtle + '\n' + '\n\n'.join(c.turtle for c in self._obj_contextes)
