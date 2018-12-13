import SentenceAssociationStrategy


class AssociationStrategyFactory:
    _strategy = []

    def __init__(self):
        self._strategy[1] = SentenceAssociationStrategy
        # TODO: later usage
        # self._strategy[2] = WindowAssociationStrategy
        # self._strategy[3] = DependencyEdgeAssociationStrategy

    def make_association_to_part(self, index, filename):
        if index == 1:
            association = Association(self._strategy[1], filename)

        # TODO: later usage
        # if index == 2:
        #    association = Association(WindowAssociationStrategy, filename, arg=2)

        # TODO: later usage
        # if index == 3:
        #    association = Association(DependencyEdgeAssociationStrategy, filename)

        # return association