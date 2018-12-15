import sys
from time import time

from AssociationTypeFactory import AssociationTypeFactory

if __name__ == '__main__':
    print 'start'
    t = time()

    # initialize factory
    factory = AssociationTypeFactory()

    test_file = "wikipedia.sample.trees.lemmatized"

    index = 2
    to_test = True

    associator = factory.make_association_for_index(index, test_file, 3)

