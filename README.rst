pyNIF-lib
=======================

What is NIF (NLP Interchange Format) ?

The NLP Interchange Format (NIF) is an RDF/OWL-based format that aims to achieve interoperability between Natural Language Processing (NLP) tools, language resources and annotations. NIF consists of specifications, ontologies and software (overview).


Documentation
=======================

[NIF Documentation](http://persistence.uni-leipzig.org/nlp2rdf/)


Supported versions
=======================

 * 2.1

Supported formats
=======================

* Turtle

Usage
=======================

0) Import and create a dataset

```
from pynif import NIFDataset


dataset = NIFDataset(uri="http://freme-project.eu")
        
```

1) Create a context

```
context = dataset.add_context(
    uri="http://freme-project.eu/doc32",
    mention="Diego Maradona is from Argentina.")

```

2) Create entries for the entities

```
context.add_bean(
    beginIndex=0,
    endIndex=14,
    taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
    score=0.9869992701528016,
    annotator='http://freme-project.eu/tools/freme-ner',
    taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
    taMsClassRef='http://dbpedia.org/ontology/SoccerManager')

context.add_bean(
    beginIndex=23,
    endIndex=32,
    taClassRef=['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
    'http://dbpedia.org/ontology/Place'],
    score=0.9804963628413852,
    annotator='http://freme-project.eu/tools/freme-ner',
    taMsClassRef='http://dbpedia.org/resource/Argentina')

nif21.bean('Diego Maradona',
           0,
           14,
           ['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
           0.9869992701528016,
           'http://freme-project.eu/tools/freme-ner',
           'http://dbpedia.org/resource/Diego_Maradona',
           'http://dbpedia.org/ontology/SoccerManager')

```

Issues
=======================

If you have any problems with or questions about this library, please contact us through a [GitHub issue](https://github.com/NLP2RDF/pyNIF-lib/issues).
