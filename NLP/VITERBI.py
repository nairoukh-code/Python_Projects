from collections import Counter
import pandas as pd
import sys

data = sys.argv[1] or open("POS.train", "r")
ready_sentence = []
sentence = []
tag_counter = Counter()
word_tag_counter = Counter()
tagi_tagj_counter = Counter()

for n in data:
    f = n.split()
    sentence.append(["start", "start"])
    for m in f:
        v = m.split("/")
        sentence.append(v)
    sentence.append(["end", "end"])
    ready_sentence.append(sentence)
    sentence = []
for q in ready_sentence:
    for p in q:
        tag_counter[p[1]] += 1
        word_tag_counter[(p[0], p[1])] += 1
for r in ready_sentence:
    for s in range(len(r) - 1):
        tagi_tagj_counter[r[s][1], r[s + 1][1]] += 1

test_data = sys.argv[2] or open("POS.test", "r")
test_set_sentence = []
ground_truth_tags = []
temp_sentence = []
temp_tag = []
pred_sent = []

for x in test_data:
    y = x.split()
    for z in y:
        g = z.split("/")
        temp_sentence.append(g[0])
        temp_tag.append((g[1]))
    test_set_sentence.append(temp_sentence)
    ground_truth_tags.append(temp_tag)
    temp_sentence = []
    temp_tag = []

distinct_tags = tag_counter.keys()

for x in test_set_sentence:
    sent_len = len(x)
    viterbi = []
    backpointer = []
    first_viterbi = {}
    first_backpointer = {}
    for tag in distinct_tags:
        if tag == "start":
            continue
        if not ((x[0], "NN") in word_tag_counter.keys()):
            word_tag_counter[(x[0], "NN")] = 1
        first_viterbi[tag] = ((word_tag_counter[(x[0], tag)]) / tag_counter[tag]) * \
                             ((tagi_tagj_counter["start", tag]) / tag_counter["start"])
        first_backpointer[tag] = "start"
    viterbi.append(first_viterbi)
    backpointer.append(first_backpointer)
    curr_best = max(first_viterbi.keys(), key=lambda tag: first_viterbi[tag])
    for words in range(1, sent_len):
        this_viterbi = {}
        this_backpointer = {}
        temp = {}
        prev_viterbi = viterbi[-1]
        for tag_1 in distinct_tags:
            if tag_1 == "start":
                continue
            for tag_2 in distinct_tags:
                if tag_2 == "start":
                    continue
                if not ((x[0], "NN") in word_tag_counter.keys()):
                    word_tag_counter[(x[words], "NN")] = 1
                prob = prev_viterbi[tag_2] * (tagi_tagj_counter[tag_2, tag_1] / tag_counter[tag_2])
                temp[tag_2] = prob
            best_previous = max(temp.keys(), key=lambda tag: temp[tag])
            this_viterbi[tag_1] = temp[best_previous] * \
                                  (word_tag_counter[x[words], tag_1] / tag_counter[tag_1])
            this_backpointer[tag_1] = best_previous
        viterbi.append(this_viterbi)
        backpointer.append(this_backpointer)
    prev_viterbi = viterbi[-1]
    prev_best = max(prev_viterbi.keys(),
                    key=lambda tag: prev_viterbi[tag] * (tagi_tagj_counter[tag, "end"] / tag_counter[tag]))
    best_score = prev_viterbi[prev_best] * (word_tag_counter[x[-1], prev_best] / tag_counter[prev_best])
    best_tagsequence = ["end", prev_best]
    backpointer.reverse()
    current_best_tag = prev_best
    for bp in backpointer:
        best_tagsequence.append(bp[current_best_tag])
        current_best_tag = bp[current_best_tag]
    best_tagsequence.reverse()
    pred_sent.append(best_tagsequence)
print(len(pred_sent))
for a in pred_sent:
    print(a)

without_tag = []
for item in pred_sent:
    item.remove("start")
    item.remove("end")
    without_tag.append(item)

# accurcy with ground truth
# print (metrics.accuracy_score(without_tag, ground_truth_tags))

tr = 0
fl = 0
for a, b in zip(without_tag, ground_truth_tags):
    for c, d in zip(a, b):
        if c == d:
            tr += 1
        else:
            fl += 1
print("true = ", tr, "false = ", fl, "score =", (tr / (tr + fl)))

test_out = []
test_out_sent = []
for a, b in zip(without_tag, test_set_sentence):
    for c, d in zip(a, b):
        test_out_sent.append(c + "/" + d)
    test_out.append(test_out_sent)
    test_out_sent = []

df = pd.DataFrame(test_out)
df.to_csv("POS.test.out")