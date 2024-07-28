# Modeling one of the OpenFGA schemas as an Ontology

[Article on Medium](https://artem-goncharov.medium.com/modelling-rebac-access-control-system-with-ontologies-and-graph-databases-1ddab8b8bcf4) with the detailed modeling process description.

[OpenFGA](https://openfga.dev/docs/fga) is a [ReBAC](https://en.wikipedia.org/wiki/Relationship-based_access_control) system based on the principles Google used to create their own ReBAC system, Zanzibar, as described in this [paper](https://storage.googleapis.com/gweb-research2023-media/pubtools/5068.pdf).

OpenFGA Schema is being modelled:

```
model  
schema 1.1  
  
type user  
  
type document  
  relations  
    define owner: [user, domain#member] or owner from parent  
    define writer: [user, domain#member] or owner or writer from parent
    define commenter: [user, domain#member] or writer or commenter from parent
    define viewer: [user, domain#member, user:*] or commenter or viewer from parent 
    define parent: [document]
  
type domain  
  relations  
    define member: [user]
```

Final ontology can be found in two formats: Turtle and RDF/XML. 
The ontology was designed usin tool [Protege](https://protege.stanford.edu). 

The ontology was tested using python script `fga_ontology_tests.py`. 
In order to run it you need to install two packages:
```
pip install owlready2
pip install rdflib
```