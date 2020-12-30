import itertools  # set iterator for next word in the file
import pandas as pd
from sklearn.preprocessing import LabelEncoder  # convert categorical variables into numerical variables
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation
import sys
# open files
sbd_train_file = sys.argv[1] or "SBD.train"
sbd_test_file = sys.argv[2] or "SBD.test"
data = open(sbd_train_file, "r")
test_data = open(sbd_test_file, "r")

# set iterator for next word in the file
list_cycle = itertools.cycle(data)
list_cycle_test = itertools.cycle(test_data)
data_features = []
test_data_features = []
test_out = []

# extract all features from train data and save it in "list of features " List
for words in data:
    word = words.split()
    if word[1][-1] == ".":
        label = word[2]
        left_word = word[1]
        list_right_words = next(list_cycle)
        right_words = list_right_words.split()
        right_word = right_words[1]
        data_features.append(
            [left_word, right_word, str(left_word[0].isupper()), str(right_word[0].isupper()),
             str(len(left_word) < 3),
             str(len(right_word) < 3), str(len(left_word) > 5), str(len(right_word) > 5), label])

# extract all features from test data and save it in "test_data_features " List
for words in test_data:
    word = words.split()
    if word[1][-1] == ".":
        label = word[2]
        left_word = word[1]
        list_right_words = next(list_cycle_test)
        right_words = list_right_words.split()
        right_word = right_words[1]
        test_data_features.append(
            [left_word, right_word, str(left_word[0].isupper()), str(right_word[0].isupper()),
             str(len(left_word) < 3),
             str(len(right_word) < 3), str(len(left_word) > 5), str(len(right_word) > 5), label])
        test_out.append([word[0], word[1]])

# place "Data & Test_Data" in pandas DataFrame
col_names = ["L word", "R word", "L cap ?", "R cap ?", "L less than 3", "R less than 3", "L more than 5",
             "R more than 5", "label"]
train_data = pd.DataFrame(data_features, columns=col_names)
test_data = pd.DataFrame(test_data_features, columns=col_names)
the_label = test_data.label


# Encoder function to Convert Pandas Categorical Data
def Encoder(df):
    columns_to_encode = list(df.select_dtypes(include=['category', 'object']))
    le = LabelEncoder()
    for feature in columns_to_encode:
        try:
            df[feature] = le.fit_transform(df[feature])
        except:
            print('Error encoding ' + feature)
    return df


train_data_encoded = Encoder(train_data)  # Encode train data set
test_data_encoded = Encoder(test_data)  # Encode test data set
all_feature_cols = ["L word", "R word", "L cap ?", "R cap ?", "L less than 3", "R less than 3", "L more than 5",
                    "R more than 5"]
core_feature_cols = ["L word", "R word", "L cap ?", "R cap ?", "L less than 3"]
my_feature_cols = ["R less than 3", "L more than 5", "R more than 5"]
all_features = train_data_encoded[all_feature_cols]  # all Features of train Data
core_feature = train_data_encoded[core_feature_cols]  # core Features of train Data
my_features = train_data_encoded[my_feature_cols]  # my Features of train Data
encoded_train_label = train_data_encoded.label
all_test = test_data_encoded[all_feature_cols]
core_test = test_data_encoded[core_feature_cols]
my_test = test_data_encoded[my_feature_cols]
encoded_test_label = test_data_encoded.label
# Create Decision Tree classifer object
clf_all = DecisionTreeClassifier()
clf_core = DecisionTreeClassifier()
clf_my = DecisionTreeClassifier()
# Train Decision Tree Classifer
all_fit = clf_all.fit(all_features, encoded_train_label)
core_fit = clf_core.fit(core_feature, encoded_train_label)
my_fit = clf_my.fit(my_features, encoded_train_label)
# Predict the response for test dataset
all_pred = all_fit.predict(all_test)
print("Accuracy for all features:", metrics.accuracy_score(encoded_test_label, all_pred), "%")
core_pred = core_fit.predict(core_test)
print("Accuracy for core features:", metrics.accuracy_score(encoded_test_label, core_pred), "%")
my_pred = my_fit.predict(my_test)
print("Accuracy for my features:", metrics.accuracy_score(encoded_test_label, my_pred), "%")
# create SBD.test.out csv file
df_pre = pd.DataFrame(all_pred)
test_out_df = pd.DataFrame(test_out, columns=["Word_#", "Word"])
le = LabelEncoder()
le.fit(the_label)
final_results = le.inverse_transform(df_pre[0])
test_out_df["my_prediction"] = final_results
test_out_df.to_csv("SBD.test.out")