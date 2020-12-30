import math
from collections import Counter
import sys

co_file = sys.argv[1] or "Collocations"
data = open(co_file, "r")
unigrams_count = Counter()
for items in data:
    item = items.split()
    for word in item:
        if word[0].isalpha() or word[0].isdecimal() and len(word) > 1:
            unigrams_count[word] += 1
# print(len(unigrams_count))

bigram_counts = Counter()
data = open("Collocations", "r")
for items in data:
    item = items.split()
    for word in range(len(item) - 1):
        if item[word][0].isalpha() or item[word][0].isdecimal() and len(item[word][0]) > 1:
            if item[word + 1][0].isalpha() or item[word + 1][0].isdecimal() and len(item[word + 1][0]) > 1:
                bigram_counts[item[word], item[word + 1]] += 1


# print(sum(bigram_counts.values()))


def chi_square(bigrams, unigrams):
    chi_values = {}
    for key, value in bigrams.items():
        bigram = key
        bi_1 = value
        N = (sum(bigrams.values()))
        if bigram[0] in unigrams:
            uni_1 = unigrams[bigram[0]]
        else:
            uni_1 = 0
        if bigram[1] in unigrams:
            uni_2 = unigrams[bigram[1]]
        else:
            uni_2 = 0
        bi_2 = (sum(bigrams.values()) - bi_1 - uni_1 - uni_2)
        o11 = bi_1
        e11 = ((bi_1 + uni_1) / N) * ((bi_1 + uni_2) / N) * N
        x1 = ((o11 - e11) ** 2) / e11
        o12 = uni_1
        e12 = ((bi_2 + uni_1) / N) * ((bi_1 + uni_1) / N) * N
        x2 = ((o12 - e12) ** 2) / e12
        o21 = uni_2
        e21 = ((bi_1 + uni_2) / N) * ((bi_2 + uni_2) / N) * N
        x3 = ((o21 - e21) ** 2) / e21
        o22 = bi_2
        e22 = ((bi_2 + uni_1) / N) * ((bi_2 + uni_2) / N) * N
        x4 = ((o22 - e22) ** 2) / e22
        chi = x1 + x2 + x3 + x4
        chi_values[bigram] = chi
    sorted_chi = sorted(chi_values.items(), key=lambda x: x[1])
    top_20 = sorted_chi[len(sorted_chi) - 20:]
    return top_20


def PMI(bigrams, unigrams):
    pmi_values = {}
    for key, value in bigrams.items():
        bigram = key
        bi_1 = value
        N = (sum(bigrams.values()))
        if bigram[0] in unigrams:
            uni_1 = unigrams[bigram[0]]
        else:
            uni_1 = 0
        if bigram[1] in unigrams:
            uni_2 = unigrams[bigram[1]]
        else:
            uni_2 = 0
        p_1 = bi_1 / N
        p_2 = uni_1 / N
        p_3 = uni_2 / N
        p_4 = (p_2 * p_3)
        if p_4 != 0:
            pmi = math.log((p_1 / p_4))
        else:
            pmi = 0
        pmi_values[bigram] = pmi
    sorted_pmi = sorted(pmi_values.items(), key=lambda x: x[1])
    top_20 = sorted_pmi[len(sorted_pmi) - 20:]
    return top_20

P = chi_square(bigram_counts, unigrams_count)
print("top 20 chi-square")
for value in P:
    print(value)

P = PMI(bigram_counts, unigrams_count)
print("top 20 PMI")
for value in P:
    print(value)