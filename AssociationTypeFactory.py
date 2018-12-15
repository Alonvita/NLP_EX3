from Association import Association
from SentenceAssociation import SentenceAssociation


class AssociationTypeFactory:
    _strategy = []

    def __init__(self):
        self._strategy = [3]
        self._strategy[0] = SentenceAssociation
        # TODO: later usage
        # self._strategy[1] = WindowAssociationStrategy
        # self._strategy[2] = DependencyEdgeAssociationStrategy

    """
        make_association_to_part(self, index, filename).
        makes the association or returns false.
    """
    def make_association_for_index(self, index, filename):
        return Association(self._strategy[index - 1], filename)

