import sys
from time import time

from AssociationTypeFactory import AssociationTypeFactory

if __name__ == '__main__':
    t = time()

    # initialize factory
    factory = AssociationTypeFactory()

    test_file = "wikipedia.sample.trees.lemmatized"

    index = 3
    to_test = True

    try:
        associator = factory.make_association_for_index(index, test_file)
    except NotImplementedError:
        print (""
               "Associations types are: \n\t"
               "1. Sentence\n\t"
               "2. Window\n\t"
               "3. Dependency Edge\n"
               "Please enter an index in the given range: 1-3")
        exit(-1)

    print("Done.")
