import pandas as pd

"""
    Target words were given in the assignment's description.
"""
TARGET_WORDS_ARRAY = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def load_words_arr_and_vec_matrix_from_csv(fp):
    """
    load_words_arr_and_vec_matrix_from_csv(fp).

    :param fp: a file path to a csv file.
    :return: a words array and a words vector matrix.
    """
    # get the number of columns
    with open(fp, 'r') as f:
        cols_count = len(f.readline().split())

    # extract from file the words and their representation as vectors
    words_arr = pd.read_csv(fp, header=None, delimiter=' ', dtype=str, usecols=[0]).values
    print 'Words loaded'
    vectors_matrix = pd.read_csv(fp, header=None, delimiter=' ', usecols=range(1, cols_count)).values
    print 'Matrix loaded'

    return words_arr, vectors_matrix


def generate_similar_words(vector, words_arr, vectors_matrix):
    """
    calc_sim(vector, words_arr, vectors_matrix).

    :param vector: a vector.
    :param words_arr: an array of words.
    :param vectors_matrix: a vectors matrix.
    :return: a list of similar words as strings
    """
    dt = vectors_matrix.dot(vector)  # calc dot-product
    sim_ids = dt.argsort()[-1:10:-1]
    return words_arr[sim_ids]


def words_to_index(words_array):
    """
    words_to_index(words).

    :param words_array: array of strings.
    :return: a dictionary representing the words indexes.
    """
    return {words_array[i][0]: i for i in range(len(words_array))}


def get_dict_word_to_vec(file_path):
    """
    get_dict_word_to_vec(filename).

    :param file_path: a path a csv file.
    :return: a dictionary of words as vectors from the TARGET_WORDS_ARRAY (see the top of this file).
    """
    # load words and vectors and create dictionary for the words
    words_array, words_matrix = load_words_arr_and_vec_matrix_from_csv(file_path)
    w2i = words_to_index(words_array)

    return {word: words_matrix[w2i[word]] for word in TARGET_WORDS_ARRAY}
