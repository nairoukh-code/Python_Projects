from collections import Counter
import pandas as pd
import sys

data =sys.argv[1] or open("POS.train", "r")
ready_sentence = []
sentence = []
tag_counter = Counter()
word_tag_counter = Counter()

for n in data:
    f = n.split()
    for m in f:
        v = m.split("/")
        sentence.append(v)
    ready_sentence.append(sentence)
    sentence = []

for q in ready_sentence:
    for p in q:
        if p[0] in word_tag_counter.keys():
            l[p[1]] += 1
            word_tag_counter[p[0]] = p[1]
        else:
            l = Counter()
            l[p[1]] += 1
            word_tag_counter[p[0]] = l
baseline_tags = {}
for n, b in word_tag_counter.items():
    if isinstance(b, str):
        baseline_tags[n] = b
    else:
        baseline_tags[n] = max(b.keys(), key=lambda tag: b[tag])


test_data = sys.argv[2] or open("POS.test", "r")
test_set_sentence = []
ground_truth_tags = []
temp_sentence = []
temp_tag = []
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

pred_sent = []
temp_pred = []
for x in test_set_sentence:
    for y in x:
        if y in baseline_tags.keys():
            temp_pred.append(baseline_tags[y])
        else:
            temp_pred.append("NN")
    pred_sent.append(temp_pred)
    temp_pred = []

# accurcy with ground truth

test_out = []
test_out_temp = []
for a, b in zip(pred_sent, test_set_sentence):
    for c, d in zip(a, b):
        test_out_temp.append(c + "/" + d)
    test_out.append(test_out_temp)
    test_out_temp = []

tr = 0
fl = 0
for a, b in zip(pred_sent, ground_truth_tags):
    for c, d in zip(a, b):
        if c == d:
            tr += 1
        else:
            fl += 1

print("true = ", tr, "false = ", fl, "score =", (tr / (tr + fl)))


df = pd.DataFrame(test_out)
df.to_csv("baseline.test.out")