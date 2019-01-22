pynif
=====

`Build Status <https://travis-ci.org/wetneb/pynif>`__

What is NIF (NLP Interchange Format) ?
--------------------------------------

The NLP Interchange Format (NIF) is an RDF/OWL-based format that aims to
achieve interoperability between Natural Language Processing (NLP)
tools, language resources and annotations. NIF consists of
specifications, ontologies and software (overview).

Documentation
-------------

`NIF Documentation <http://persistence.uni-leipzig.org/nlp2rdf/>`__

Supported NIF versions
----------------------

-  2.1

Supported RDF formats
---------------------

-  `All the formats supported by
   rdflib <https://rdflib.readthedocs.io/en/stable/plugin_parsers.html>`__

Usage
-----

0) Import and create a collection

::

   from pynif import NIFCollection


   collection = NIFCollection(uri="http://freme-project.eu")
           

1) Create a context

::

   context = collection.add_context(
       uri="http://freme-project.eu/doc32",
       mention="Diego Maradona is from Argentina.")

2) Create entries for the entities

::

   context.add_phrase(
       beginIndex=0,
       endIndex=14,
       taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
       score=0.9869992701528016,
       annotator='http://freme-project.eu/tools/freme-ner',
       taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
       taMsClassRef='http://dbpedia.org/ontology/SoccerManager')

   context.add_phrase(
       beginIndex=23,
       endIndex=32,
       taClassRef=['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
       'http://dbpedia.org/ontology/Place'],
       score=0.9804963628413852,
       annotator='http://freme-project.eu/tools/freme-ner',
       taMsClassRef='http://dbpedia.org/resource/Argentina')

3) Finally, get the output with the format that you need

::

   generated_nif = collection.dumps(format='turtle')
   print(generated_nif)

You can then parse it back:

::

   parsed_collection = NIFCollection.loads(generated_nif)

   for context in parsed_collection.contexts:
      for phrase in context.phrases:
          print(phrase)

Issues
------

If you have any problems with or questions about this library, please
contact us through a `GitHub
issue <https://github.com/NLP2RDF/pyNIF-lib/issues>`__.

Maintainers
-----------


