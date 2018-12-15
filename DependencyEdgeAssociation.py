from IAssociationType import IAssociationType

HEAD = 0
WORD = 1
TAG = 2


class DependencyEdgeAssociation(IAssociationType):
    def __init__(self):
        IAssociationType.__init__(self)

    def init_count_data_structures(self, fp, context_type):
        preposition = {'IN'}
        all_context_type = preposition.union(context_type)

        print ('Initializing count data-structs for Dependency Edge Association')

        with open(fp, 'r') as file_f:
            sentence = []
            for line in file_f:
                split_line = line.split()

                if len(split_line) == 0:  # reached end of sentence
                    self.give_sentence_features(sentence, preposition)
                    sentence = []
                else:
                    if split_line[4] in all_context_type:
                        lemma = split_line[2]
                        sentence.append((int(split_line[6]), lemma, split_line[4]))
                    else:
                        sentence.append((-1,))  # to keep the token number

            # when the file don't end with empty line:
            if len(sentence) > 0:
                self.give_sentence_features(sentence, preposition)

        print ('Done Counting.')

    """
        get_lemma_id(self, lemma).
        get the lemma ID for a given lema.
    """
    def get_lemma_id(self, lemma):
        if lemma not in self._words_map:
            # map the word to a number that represents its id
            self._words_map[lemma] = len(self._words_map)
        return self._words_map[lemma]

    """
        give_sentence_features(self, sentence, preposition).
        
    """
    def give_sentence_features(self, sentence, preposition):
        # tree = Node.buildSentenceTree(sentence)
        for tup in sentence:  # tup == (head_id, word, tag)
            if tup[HEAD] > 0 and tup[TAG] not in preposition:  # skip on root and for words that not context_type (==-1)
                word_id = self.get_lemma_id(tup[WORD])
                father = sentence[tup[HEAD] - 1]

                prepositions = []
                if father[HEAD] == -1:
                    continue

                right = True

                while father[TAG] in preposition:
                    prepositions.append(father[WORD])
                    father = sentence[father[HEAD] - 1]

                    if father[HEAD] == -1:
                        right = not right
                        break
                if not right:
                    continue

                feature = ">" + father[TAG] + "|" + father[WORD]
                feature_id = self.get_lemma_id(feature)
                self._pair_count_dict[word_id][feature_id] += 1
                self._targets_count[word_id] += 1

                feature = tup[TAG] + "|" + tup[WORD] + "<"
                feature_id = self.get_lemma_id(feature)
                father_id = self.get_lemma_id(father[WORD])

                self._pair_count_dict[father_id][feature_id] += 1
                self._targets_count[father_id] += 1
                if len(prepositions) > 0:
                    feature = ">" + father[TAG] + "|" + father[WORD]
                    for pre in prepositions:
                        feature = ">" + pre + feature
                    feature_id = self.get_lemma_id(feature)
                    self._pair_count_dict[word_id][feature_id] += 1
                    self._targets_count[word_id] += 1

                    feature = tup[TAG] + "|" + tup[WORD] + "<"
                    for pre in prepositions:
                        feature = feature + pre + "<"
                    word_id = self.get_lemma_id(father[WORD])
                    self._targets_count[word_id] += 1
                    feature_id = self.get_lemma_id(feature)
                    self._pair_count_dict[word_id][feature_id] += 1
