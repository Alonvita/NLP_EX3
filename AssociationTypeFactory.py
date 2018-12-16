from Association import Association
from BagOfWordsAssociation import WindowAssociation
from SentenceAssociation import SentenceAssociation
from DependencyEdgeAssociation import DependencyEdgeAssociation


class AssociationTypeFactory:
    _strategy = []

    def __init__(self):
        self._strategy = [
            SentenceAssociation,  # Sentence association as [0]
            WindowAssociation,  # Window association as [1]
            DependencyEdgeAssociation,  # Dependency Edge association as [2]
        ]

    def make_association_for_index(self, index, filename, arg=None):
        """
            make_association_to_part(self, index, filename).
            makes the association or returns false.
        """
        if 1 <= index <= 3:
            return Association(self._strategy[index - 1], filename, arg)

        raise NotImplementedError

