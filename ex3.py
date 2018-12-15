import sys
from time import time
from VectorBuilder import VectorBuilder

from AssociationTypeFactory import AssociationTypeFactory

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']
MAX_VEC_LEN = 20


def write_features_to_file(ex_part, input_ass):
    f = open('./features/features_part' + str(ex_part) + '.txt', 'w')
    for target_word in TARGET_WORDS:
        f.write(target_word + ':\n')
        for feat in input_ass.get_features_for(input_ass.get_word_id(target_word)):
            f.write('\t' + input_ass.get_word_from_id(feat) + '\n')
        f.write('\n')

    f.close()
    exit(0)


def write_first_order_to_file(ex_part, vector):
    f = open('./features/first_order_for_part' + str(ex_part) + '.txt', 'w')
    for target_word in TARGET_WORDS:
        local_association = vector.get_association()

        f.write(target_word + ':\n')
        vec = sorted(vector.vectors[local_association.get_word_id(target_word)])

        if len(vec) > MAX_VEC_LEN:
            vec = vec[-MAX_VEC_LEN:]
        else:
            print str(len(vec))+" = " + target_word

        for feat in vec:
            f.write('\t' + local_association.get_word_from_id(feat) + '\n')
        f.write('\n')

    f.close()
    exit(0)


if __name__ == '__main__':
    t = time()

    # initialize factory
    factory = AssociationTypeFactory()

    test_file = "wikipedia.sample.trees.lemmatized"

    index = 3
    init_testing = False

    try:
        association = factory.make_association_for_index(index, test_file)
    except NotImplementedError:
        print (""
               "Associations types are: \n\t"
               "1. Sentence\n\t"
               "2. Window\n\t"
               "3. Dependency Edge\n"
               "Please enter an index in the given range: 1-3")
        exit(-1)

    vec_builder = VectorBuilder(association)

    if init_testing:
        association.test()
        vec_builder.test_pmi()

    vec_builder.build_all_vectors()
    write_first_order_to_file(index, vec_builder)
    vec_builder.find_similarities(TARGET_WORDS, 'result_part' + str(index) + ".txt")

    print("Done.")
