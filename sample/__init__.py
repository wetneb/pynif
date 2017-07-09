import NIF21

def main():
    nif21 = NIF21.NIF21()

    nif21.context("http://freme-project.eu", 0, 33, "Diego Maradona is from Argentina.")

    nif21.bean('Diego Maradona',
               0,
               14,
               ['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person',
                'http://nerd.eurecom.fr/ontology#Person'],
               0.9869992701528016,
               'http://freme-project.eu/tools/freme-ner',
               'http://dbpedia.org/resource/Diego_Maradona',
               'http://dbpedia.org/ontology/SoccerManager')

    nif21.bean('Argentina',
               23,
               32,
               ['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
                'http://dbpedia.org/ontology/Place'],
               0.9804963628413852,
               'http://freme-project.eu/tools/freme-ner',
               'http://dbpedia.org/resource/Argentina',
               None)

    print nif21.turtle()
