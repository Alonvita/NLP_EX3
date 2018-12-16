import sys
from time import time

import Utils


def main():
    t = time()
    print 'Running word2vec_feature.py. Timestamp: ', time()

    if len(sys.argv) == 1:
        words_fp = "WordsAndContexts/bow5.words"  # testing purposes...
    else:
        words_fp = sys.argv[1] + '.words'

    file_path_to_name = words_fp.split(".")[0]
    filename = file_path_to_name.split("/")[1]

    # load words and vectors and create dictionary for the words
    target_word_to_vec = Utils.get_dict_word_to_vec(words_fp)

    print 'Loading words file. Timestamp: ', time() - t
    t = time()

    # load contexts and vectors and create dictionary for the words
    contexts_filename = file_path_to_name + '.contexts'
    contexts, matrix = Utils.load_words_arr_and_vec_matrix_from_csv(contexts_filename)
    print 'Context file timestamp:', time() - t
    t = time()

    out = open('word2vec2_features_' + filename + '.txt', 'w')

    for word in Utils.TARGET_WORDS_ARRAY:  # for each target word
        out.write(word + ':\n')  # write it to file
        word_as_vec = target_word_to_vec[word]  # get the word as a vector

        # get the top 10 similar words to it
        top_10_similar_words = [word[0] for word in Utils.generate_similar_words(word_as_vec, contexts, matrix)[:11]]

        # and write them to file
        for sim_word in top_10_similar_words:
            out.write('\t' + sim_word + '\n')
        out.write('\n')

    out.close()
    print 'Similarities found. Timestamp: ', time() - t


if __name__ == '__main__':
    main()
