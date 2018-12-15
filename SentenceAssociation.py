from IAssociationType import IAssociationType


class SentenceAssociation(IAssociationType):
    def __init__(self):
        IAssociationType.__init__(self)

    def init_count_data_structures(self, fp, context_type):
        print("Initializing count data-structs for Sentence Association")

        with open(fp, 'r') as file_f:
            # set sentence to an empty set
            sentence = set()

            # open file
            for line in file_f:
                # split line
                split_line = line.split()
                # check if end of file reached
                if len(split_line) == 0:
                    for word in sentence:
                        dif = sentence.difference({word})  # make a difference of the sentence - word
                        self._targets_count[word] += len(dif)  # add the length to the targets count
                        for context in dif:
                            self._pair_count_dict[word][context] += 1
                    sentence.clear()  # clear the sentence
                else:
                    if split_line[4] in context_type:  # check if the word is of valid context
                        lemma = split_line[2]
                        if lemma not in self._words_map:
                            # map the new registry for the word
                            self._words_map[lemma] = len(self._words_map)
                        sentence.add(self._words_map[lemma])  # add to sentence

            # file did not end with empty lines
            if len(sentence) > 0:
                for word in sentence:
                    dif = sentence.difference({word})
                    self._targets_count[word] += len(dif)
                    for context in dif:
                        self._pair_count_dict[word][context] += 1
                sentence.clear()

            print("Done counting...")

    def get_words_count(self):
        return self._words_count

    def get_words_map(self):
        return self._words_map

    def get_target_count(self):
        return self._targets_count

    def get_features_count(self):
        return self._features_count

    def get_pair_count_dict(self):
        return self._pair_count_dict

    def add_words_count(self, count):
        self._words_count += count
