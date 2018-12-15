from time import time
from collections import defaultdict

THRESHOLD = 100
FEATURES_PER_WORD = 50


class Association:
    """ holds an Association Type, and performs generic functions on it """
    def __init__(self, association_type, fp, arg=None):
        if arg is None:
            self.association_type = association_type()
        else:
            self.association_type = association_type(arg)

        # Content words are only verbs, nouns, adjectives, adverbs
        context_type = {  # tag from Penn Tree bank II tag set
            'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG', 'WRB',  # verbs
            'MD', 'NN', 'NNS', 'NNP', 'NNPS',  # nouns
            'PRP', 'PRP$',  # pronoun
            'JJ', 'JJR', 'JJS',  # adjectives
            'RB', 'RBR', 'RBS', 'RP'  # adverbs
        }

        self.association_type.init_count_data_structures(fp, context_type)

        self.recovery_filename = 'recovery_file'
        self._filter()

    def _filter(self):
        print ('Filtering uncommon target words.')
        # Local Variables
        ass_type = self.association_type

        for word_id in ass_type.get_target_count().keys():
            if ass_type.get_target_count()[word_id] < THRESHOLD and word_id in ass_type.get_pair_count_dict():
                del ass_type.get_pair_count_dict()[word_id]
            else:
                # counting: #(*,att) after filtering
                for feature in ass_type.get_pair_count_dict()[word_id]:
                    ass_type.get_features_count()[feature] += ass_type.get_pair_count_dict()[word_id][feature]

                # counting #(*,*)
                ass_type.add_words_count(ass_type.get_target_count()[word_id])

        print ('Filtering is Done.')

    """
        get_word_id(self, word).
        return the word id from the words map, or False if doesn't exist.
    """
    def get_word_id(self, word):
        # Local Variables
        ass_type = self.association_type

        if word in ass_type.word_mapper:
            return ass_type.word_mapper[word]
        else:
            return False

    """
        get_all_common_targets_ids(self).
        return all of the word's filtered.
    """
    def get_all_common_targets_ids(self):
        commons = self.association_type.pair_counts.keys()
        return commons

    """
        get_word_from_id(self, word_id).
        self explanatory.
    """
    def get_word_from_id(self, word_id):
        strategy = self.association_type
        return strategy.word_mapper.keys()[strategy.word_mapper.values().index(word_id)]

    """
        get_target_count(self, target_id).
        return the target's count for a given id (0 if doesn't exist).
    """
    def get_target_count(self, target_id):
        # Local Variables
        ass_type = self.association_type  # (word, *) or 0

        # check if id exists in the words count
        if target_id in ass_type.targets_count:
            return ass_type.targets_count[target_id]  # if so, get the count for it
        return 0

    """
        get_pair_count(self, target_id, feature_id).
        return the pairs count for a given id (0 if doesn't exist).
    """
    def get_pair_count(self, target_id, feature_id):
        # Local Variables
        ass_type = self.association_type  # (word, feature)
        if target_id in ass_type.pair_counts and feature_id in ass_type.pair_counts[target_id]:
            return ass_type.pair_counts[target_id][feature_id]
        return 0

    """
        get_total_count(self).
        get the words count for this association type.
    """
    def get_total_count(self):
        """ #(*,*) """
        return self.association_type.get_words_count()

    """
        get_feature_count(self, feature_id).
        return the features count for a given id (0 if doesn't exist).
    """
    def get_feature_count(self, feature_id):
        ass_type = self.association_type  # (*, feature)

        if feature_id in ass_type.features_count:
            return ass_type.features_count[feature_id]
        return 0

    """
        get_features_for(self, target_id).
        return all of the features for a given ID, or an empty dict.
    """
    def get_features_for(self, target_id):
        # Local Variables
        ass_type = self.association_type

        if target_id in ass_type.pair_counts:
            return map(lambda x: x[0], ass_type.pair_counts[target_id].most_common(FEATURES_PER_WORD))
        else:
            return {}

    """
        clean_association(self).
    """
    def clean_association(self):
        self.association_type.clean_mem()

    """
        recover_file(self).
        :return a dictionary of words taken from attributes
    """
    def recover_file(self):
        t = time()
        att_to_word = defaultdict(list)

        with open(self.recovery_filename, 'r') as file_f:
            for line in file_f:
                split_line = line.split()
                feature_id = int(split_line[0])
                att_to_word[feature_id].append(int(split_line[1]))
            file_f.close()

        import os
        os.remove(self.recovery_filename)
        print 'time for recover-file:', time() - t
        return att_to_word

    """
        test(self).
    """
    def test(self):
        # Local Variables
        ass_type = self.association_type
        pair_counts = ass_type.get_pair_count_dict()
        targets_count = ass_type.get_target_count()

        for word_id in pair_counts.keys():
            if len(list(pair_counts[word_id].elements())) != targets_count[word_id]:
                print ('---')
                print (self.get_word_from_id(word_id))
                print (pair_counts[word_id])
                print (len(list(pair_counts[word_id].elements())))
                print (targets_count[word_id])

    """
        get_structure_pair_counts(self).
    """
    def get_association_pair_dict(self):
        return self.association_type.get_pair_count_dict()

    """
        get_features_count(self).
    """
    def get_features_count(self):
        return self.association_type.get_features_count()
