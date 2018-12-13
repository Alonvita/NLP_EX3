import sys
from time import time

from AssociationStrategyFactory import AssociationStrategyFactory

if __name__ == '__main__':
    print 'start'
    t = time()

    # initialize factory
    factory = AssociationStrategyFactory()

    part = 3
    to_test = True

    associator = factory.make_association_to_part(part, sys.argv[1])
