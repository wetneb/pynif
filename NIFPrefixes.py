class NIFPrefixes:
    def __init__(self):
        self._XSD = '@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .\n'
        self._ITSRDF = '@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .\n'
        self._NIF = '@prefix nif:   <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .\n'

    @property
    def turtle(self):
        return self._XSD + self._ITSRDF + self._NIF
