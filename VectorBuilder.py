from collections import Counter
from time import time
import numpy as np

TOP_SIMILARITY_CAP = 20


class VectorBuilder:
    def __init__(self, association):
        self.association = association
        self.vectors = {}

    def calc_pmi(self, target_id, feature_id):
        """
        calc_PMI(self, target_id, feature_id).

        :param target_id: a target's id
        :param feature_id: a featuer's id
        :return: the PMI calculation for the target id and feature id
        """
        # p(a, b) where a is a word and b is a feature
        numerator = float(self.association.get_pair_count(target_id, feature_id)) / self.association.get_total_count()

        # p(a) * p(b)
        denominator = float(self.association.get_feature_count(feature_id)) / self.association.get_total_count()
        denominator *= float(self.association.get_target_count(target_id)) / self.association.get_total_count()

        if denominator == 0 or numerator == 0:
            return 0
        else:
            return np.log(numerator / denominator)

    def get_association(self):
        """
        get_association(self).
        :return: the association held by this vector
        """
        return self.association

    def make_vector_for(self, target_id, recovery_file):
        """
        :return a dictionary mapping feature to pmi-value (target_id -> feature_id)
        """
        vector = dict()
        features = self.association.get_features_for(target_id)
        for feature_id in features:
            recovery_file.write(str(feature_id) + " " + str(target_id) + "\n")
            pmi_result = self.calc_pmi(target_id, feature_id)
            if pmi_result > 0:
                vector[feature_id] = pmi_result
        return vector

    def build_all_vectors(self):
        """
        build_all_vectors(self).
        """
        print "Building all vectors."
        recovery_file = open(self.association.recovery_filename, 'w')

        for target_id in self.association.get_all_common_targets_ids():
            self.vectors[target_id] = self.make_vector_for(target_id, recovery_file)

        recovery_file.close()
        self.association.clean_association()
        print ('vectors building is done!')

    def cosine(self, lhs_target_id, rhs_target_id):
        """
        cosine(self, target_id1, target_id2).

        :param lhs_target_id: a target id
        :param rhs_target_id: a target id
        :return:
        """
        features1 = set(self.vectors[lhs_target_id].keys())  # take lhs target_id key's
        features2 = set(self.vectors[rhs_target_id].keys())  # take rhs target_id key's

        intersection = features1.intersection(features2)  # find the intersection

        # Local Variables
        numerator = 0.0
        left_denominator = 0.0
        right_denominator = 0.0

        for feature in intersection:
            numerator += float(self.vectors[lhs_target_id][feature]) * self.vectors[rhs_target_id][feature]
            right_denominator += self.vectors[lhs_target_id][feature] ** 2
            left_denominator += self.vectors[rhs_target_id][feature] ** 2

        return numerator / np.sqrt(right_denominator * left_denominator)

    def test_pmi(self):
        """
        test_pmi(self).
        """
        p_target = 0.0
        p_feature = 0.0
        p_pair = 0.0

        pairs_dict = self.association.get_association_pair_dict()
        features_count = self.association.get_features_count_struct()

        for word_id in pairs_dict.keys():
            p_target += float(self.association.get_target_count(word_id)) / self.association.get_total_count()
            for feature_id in pairs_dict[word_id]:
                p_pair += float(
                    self.association.get_pair_count(word_id, feature_id)) / self.association.get_total_count()

        for feature_id in features_count:
            p_feature += float(self.association.get_feature_count(feature_id)) / self.association.get_total_count()

        if np.isclose([p_target], [1.0]) and np.isclose([p_feature], [1.0]) and np.isclose([p_pair], [1.0]):
            print ('PMI test Succeeded!')
        else:
            print ('PMI test failed:')
            print ('P_target: ' + str(p_target))
            print ('P_feature: ' + str(p_feature))
            print ('P_pair: ' + str(p_pair))

    def calc_sim(self, word):
        """
        calc_sim(self, word).
        :param word: a word.
        """
        word_id = self.association.get_word_id(word)
        sim_vec = Counter()
        for v_id in self.vectors:
            sim_vec[v_id] = self.cosine(word_id, v_id)
        sim_vec = sim_vec.most_common(20)
        as_words = [(self.association.get_word_from_id(vec_id[0]), vec_id[1]) for vec_id in sim_vec]
        for item in as_words:
            print item

    def find_similarities(self, words, result_filename):
        """ find top-n similar-words to the given words, writes the results in the file specified """

        print 'applying efficient algorithm'
        t = time()

        f = open(result_filename, 'w')
        att_to_words = self.association.recover_file()

        for u in words:
            f.write(u + ':\n')
            u = self.association.get_word_id(u)
            dt = Counter()  # word-v to score, actually similarity-of-u-and-v

            u_vec = self.vectors[u]
            for att in u_vec:
                one = u_vec[att]
                for v in att_to_words[att]:
                    if v not in self.vectors or u == v:
                        continue
                    two = 0
                    if att in self.vectors[v]:
                        two = self.vectors[v][att]
                    dt[v] += one * two

            top_n = [(self.association.get_word_from_id(word[0]), word[1]) \
                     for word in dt.most_common(TOP_SIMILARITY_CAP)]
            for item in top_n:
                f.write('\t' + item[0] + '\n')
            f.write('\n')

        f.close()
        print 'time to find words:', time() - t  # should take about 60-sec
