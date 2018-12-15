from IAssociationType import IAssociationType


class WindowAssociation(IAssociationType):
    def __init__(self, window_size):
        IAssociationType.__init__(self)
        self.window_size = window_size

    def init_count_data_structures(self, fp, context_type):
        print("Initializing count data-structs for Window Association")
        # Local Variables
        window_size = self.window_size
        window_context_len = 2 * window_size

        with open(fp, 'r') as file_f:
            sentence = []
            for line in file_f:
                split_line = line.split()
                if len(split_line) == 0:  # reached end of sentence
                    for i in range(window_size, len(sentence) - window_size):
                        word = sentence[i]  # get the word
                        self._targets_count[word] += window_context_len  # add window context len to targets count
                        relevant_indices = range(i - window_size, i + window_size + 1)  # set relevant indices
                        relevant_indices.remove(i)  # remove i from the relevant indices
                        for context_index in relevant_indices:
                            self._pair_count_dict[word][sentence[context_index]] += 1

                    del sentence
                    sentence = []
                else:
                    if split_line[4] in context_type:
                        lemma = split_line[2]
                        if lemma not in self._words_map:
                            # map the word to a number that represents its id
                            self._words_map[lemma] = len(self._words_map)
                        sentence.append(self._words_map[lemma])

            # when the file don't end with empty line:
            if len(sentence) > 0:
                for i in range(window_size, len(sentence) - window_size):
                    word = sentence[i]
                    self._targets_count[word] += window_context_len
                    relevant_indices = range(i - window_size, i + window_size + 1)
                    relevant_indices.remove(i)
                    for context_index in relevant_indices:
                        self._pair_count_dict[word][sentence[context_index]] += 1

                del sentence

        print ('Done Counting.')
