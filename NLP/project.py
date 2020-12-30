from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import pandas as pd
from nltk.corpus import words
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# open and clean true and fake tweets and split them into train and test data
true_tweets = open("genuine_tweets.csv", errors='ignore')
tweets_collection = []
for tweet in true_tweets:
    if len(tweet) > 0:
        tweet_split = tweet.split(",")
        if len(tweet_split) > 2:
            if tweet_split[1] != "“just posted a photo”":
                tweets_collection.append([tweet_split[1], "true"])
fake_tweets = open("fake_tweets.csv", errors='ignore')
fake_tweets_collection = []
for tweet in fake_tweets:
    if len(tweet) > 0:
        tweet_split = tweet.split(",")
        if len(tweet_split) > 2:
            if tweet_split[2] != "“just posted a photo”":
                tweets_collection.append([tweet_split[2], "fake"])

tweet_train, tweet_test = train_test_split(tweets_collection, train_size=0.8)

# extract feature vector

train_tweet_features = []
test_tweet_features = []
stopWords = set(stopwords.words('english'))

for tweet in tweet_train:
    stopword_occur = 0
    capital_occur = 0
    number_occur = 0
    eng_word_occur = 0
    mention = 0
    for word in tweet[0]:
        if word in stopWords:
            stopword_occur += 1
        if word.isupper():
            capital_occur += 1
        if word.isdecimal():
            number_occur += 1

        if word[0] == "@":
            mention += 1
    train_tweet_features.append([len(tweet[0]), stopword_occur, capital_occur, number_occur, mention, tweet[1]])

for tweet in tweet_test:
    stopword_occur = 0
    capital_occur = 0
    number_occur = 0
    eng_word_occur = 0
    mention = 0
    for word in tweet[0]:
        if word in stopWords:
            stopword_occur += 1
        if word.isupper():
            capital_occur += 1
        if word.isdecimal():
            number_occur += 1

        if word[0] == "@":
            mention += 1
    test_tweet_features.append([len(tweet[0]), stopword_occur, capital_occur, number_occur, mention, tweet[1]])

# place "Data & Test_Data" in pandas DataFrame

col_names = ["length of tweet", "stopwords occur", "capital occur", "number_occur", "mention", "label"]
train_data = pd.DataFrame(train_tweet_features, columns=col_names)
test_data = pd.DataFrame(test_tweet_features, columns=col_names)
train_data.to_csv("train_data")
test_data.to_csv("test_data")

#combine and shuffle data for k-folds
Tweets=pd.concat([train_data,test_data])

Tweets = Tweets.sample(frac = 1)
Tweets=Tweets.reset_index(drop=True)

# Get Features
features=[]

for i in range(len(Tweets.columns)-1):
    features.append(Tweets.columns[i])

#Split into folds and preform Evaluation
Folds = KFold(n_splits=5)
i=1
for train,test in Folds.split(Tweets):
    print("Fold %d"%i)
    X=Tweets.iloc[train][features]
    Y=Tweets.iloc[train]['label']
    Xtest=Tweets.iloc[test][features]
    Ytest=Tweets.iloc[test]['label']
    model=DecisionTreeClassifier()
    model.fit(X,Y)
    Ypred=model.predict(Xtest)
    print("accuracy_Score %2fPERCENT"%(accuracy_score(Ytest,Ypred)))
    i=i+1