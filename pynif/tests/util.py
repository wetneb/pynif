from rdflib.graph import Graph
from rdflib.compare import isomorphic
from rdflib.compare import graph_diff

def turtle_equal(a, b):
    """
    Given two strings representing turtle-encoded RDF,
    check whether they represent the same graph.
    """
    ga = Graph().parse(format='turtle',data=a)
    for x, y, z in ga:
        print((x,y,z))
    gb = Graph().parse(format='turtle',data=b)
    eq = isomorphic(ga, gb)
    if not eq:
        both, first, second = graph_diff(ga, gb)
        print("Present in both:")
        print(both)
        print("Present in first:")
        print(first)
        print("Present in second:")
        print(second)
    return eq
