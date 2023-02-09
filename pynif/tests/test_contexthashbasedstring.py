
import unittest

from pynif.tools.context_hash_based_string import context_hash_based_string

class NIFContextHashBasedStringTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sample_text1 = "Diego Maradona is from Argentina."
        cls.sample_text2 = "    Primary Navigation Secondary Navigation Search: Nearly 60 militants killed in southern Afghanistan Tue Oct 7, 9:14 AM ET KABUL (Reuters) - U.S.-led coalition and Afghan security forces killed nearly 60 militants during separate clashes in southern Afghanistan, the U.S. military and a police official said Tuesday. Violence has surged in the war-torn country with some 3,800 people, a third of them civilians, killed as a result of the conflict by the end of July this year, according to the United Nations. U.S.-led coalition and Afghan security forces killed 43 militants during heavy fighting in Qalat district of southern Zabul province Sunday, the U.S. military said in a statement Tuesday. \"ANSF (Afghan National Security Forces ) and coalition forces on a patrol received heavy weapons, machine gun and sniper fire from militants in multiple locations,\" the U.S. military said in a statement. The combined forces responded with small arms fire , rocket propelled grenades and close air support , killing the militants, it said. No Afghan or U.S.-led troops were killed or wounded during incident, it said. In a separate incident, Afghan and international troops killed 16 Taliban insurgents and wounded six more during a gun battle in Nad Ali district of southern Helmand province on Monday, provincial police chief Asadullah Sherzad told Reuters. (Writing by Jonathon Burch; Editing by Bill Tarrant)"
        cls.sample_original_uri1 = 'http://freme-project.eu'
        cls.sample_original_uri2 = "http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc"

    def test_create_ContextHashBasedString(self):
        uri1 = context_hash_based_string(self.sample_text1, self.sample_original_uri1)
        uri2 = context_hash_based_string(self.sample_text2, self.sample_original_uri2)
        self.assertEqual('http://freme-project.eu#hash_0_33_cf35b7e267d05b7ca8aba0651641050b_Diego%20Maradona%20is%20fr', uri1)
        self.assertEqual('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_4_1411_0d65523ef72343af915f29206bfde1b8_%20%20%20%20Primary%20Navigati', uri2)

    def test_create_ContextHashBasedString_with_index(self):
        uri1 = context_hash_based_string(self.sample_text1, self.sample_original_uri1,beginIndex=0, endIndex=14)
        uri2 = context_hash_based_string(self.sample_text2, self.sample_original_uri2, beginIndex=91, endIndex=102)
        self.assertEqual('http://freme-project.eu#hash_10_14_d18575292bcf716916eb99eb8927377f_Diego%20Maradona', uri1)
        self.assertEqual('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_10_11_0fe40301646263d200012262413c878a_Afghanistan', uri2)

    def test_create_ContextHashBasedString_with_context_length(self):
        uri1 = context_hash_based_string(self.sample_text1, self.sample_original_uri1,beginIndex=0, endIndex=14,context_length=15)
        uri11 = context_hash_based_string(self.sample_text1, self.sample_original_uri1,beginIndex=0, endIndex=14,context_length=50)
        uri2 = context_hash_based_string(self.sample_text2, self.sample_original_uri2, beginIndex=91, endIndex=102,context_length=20)
        self.assertEqual('http://freme-project.eu#hash_15_14_6fa991de875b46406ce4f216e5715310_Diego%20Maradona', uri1)
        self.assertEqual('http://freme-project.eu#hash_19_14_158118325b076b079d3969108872d855_Diego%20Maradona', uri11)
        self.assertEqual('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_20_11_941d9088048c1195724047492080b60d_Afghanistan', uri2)

    def test_create_ContextHashBasedString_safe(self):
        uri1 = context_hash_based_string(self.sample_text1, self.sample_original_uri1,beginIndex=0, endIndex=14, safe=True)
        uri2 = context_hash_based_string(self.sample_text2, self.sample_original_uri2, beginIndex=91, endIndex=102, safe=True)
        self.assertEqual('http://freme-project.eu#hash_10_14_d18575292bcf716916eb99eb8927377f_Diego%20Maradona_0_14', uri1)
        self.assertEqual('http://www.cse.iitb.ac.in/~soumen/doc/CSAW/doc#hash_10_11_0fe40301646263d200012262413c878a_Afghanistan_91_102', uri2)


if __name__ == '__main__':
    unittest.main()
