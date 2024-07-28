from owlready2 import *
from rdflib import Graph
import unittest
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

ontology_path = os.path.join(current_dir, "open_fga_ontology_final.ttl")
g = Graph()
g.parse(ontology_path, format="turtle")

# Serialize to RDF/XML
rdfxml_path = os.path.join(current_dir, "test_ontology.xml")
g.serialize(destination=rdfxml_path, format="xml")

onto = get_ontology(rdfxml_path).load()
sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)

class TestOntology(unittest.TestCase):

    def setUp(self):
        # Create test individuals
        self.article1 = onto.Document("Article-1")
        self.article11 = onto.Document("Article-1-1")
        self.article111 = onto.Document("Article-1-1-1")
        self.public_article = onto.PublicDocument("PublicArticle-1")
        self.admins = onto.Domain("Admins")
        # Article-1 is parent of Article-1-1
        self.article1.PARENT.append(self.article11)
        # Article-1-1 is parent of Article-1-1-1
        self.article11.PARENT.append(self.article111)

        # Admins are WRITER for Article-1-1
        self.admins.WRITER_DOMAIN.append(self.article11)

        self.artem = onto.User("Artem") # owns Article-1
        self.artem.OWNER.append(self.article1)
        
        self.john = onto.User("John") # member of admins domain
        self.john.MEMBER.append(self.admins)

        self.kira = onto.User("Kira") # doesn't have any relationships

        # Synchronize the reasoner after adding individuals to compute relationships
        sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)

    def test_parent_transitive(self):
        self.assertIn(self.article111, self.article1.PARENT)

    def test_owner_transitively_owns_children_documents(self):
        self.assertIn(self.article11, self.artem.OWNER)
        self.assertIn(self.article111, self.artem.OWNER)

    def test_admin_member_can_write_documents(self):
        self.assertIn(self.article11, self.john.WRITER)
        self.assertIn(self.article111, self.john.WRITER) # transitively over documents hierarchy
        self.assertNotIn(self.article1, self.john.WRITER) # no way to go upwards of the documents hierarchy

    def test_all_users_viewers_of_public_documents(self):
        self.assertIn(self.public_article, self.kira.WRITER)

    def test_owner_also_write_children_documents(self):
        self.assertIn(self.article1, self.artem.WRITER)
        self.assertIn(self.article11, self.artem.WRITER)
        self.assertIn(self.article111, self.artem.WRITER)

    def test_writer_also_commenter_children_documents(self):
        self.assertIn(self.article1, self.artem.COMMENTER)
        self.assertIn(self.article11, self.artem.COMMENTER)
        self.assertIn(self.article111, self.artem.COMMENTER)
        self.assertIn(self.article11, self.john.COMMENTER)
        self.assertIn(self.article111, self.john.COMMENTER)

    def test_commenter_also_viewer_children_documents(self):
        self.assertIn(self.article1, self.artem.VIEWER)
        self.assertIn(self.article11, self.artem.VIEWER)
        self.assertIn(self.article111, self.artem.VIEWER)
        self.assertIn(self.article11, self.john.VIEWER)
        self.assertIn(self.article111, self.john.VIEWER)

if __name__ == "__main__":
    unittest.main()