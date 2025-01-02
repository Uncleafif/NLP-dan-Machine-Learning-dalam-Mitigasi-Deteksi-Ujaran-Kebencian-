# -*- coding: utf-8 -*-
"""41220093_Muhammad Afif_Penggunaan NLP dan Machine Learning dalam Mitigasi Deteksi Ujaran Kebencian yang Berbahaya secara Online di Tweet

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EKqtB-Ko_Nk2qGN2Gl7GH_jhqTiODHmX
"""

from google.colab import files
import pandas as pd
import io

# Mengunggah file CSV dari komputer Anda
upload_files = files.upload()

# Membaca file CSV yang diunggah
for filename in upload_files.keys():
    data = pd.read_csv(io.StringIO(upload_files[filename].decode('utf-8')))

# Menampilkan lima baris pertama dari data
print(data.head())

# Menampilkan ukuran data (jumlah baris dan kolom)
print("Ukuran Data:", data.shape)

from google.colab import files
import pandas as pd
import io

# Mengunggah file CSV dari komputer Anda
upload_files = files.upload()

# Membaca file CSV yang diunggah
for filename in upload_files.keys():
    data = pd.read_csv(io.StringIO(upload_files[filename].decode('utf-8')))

# Menampilkan lima baris pertama dari data
print(data.head())

# Menampilkan ukuran data (jumlah baris dan kolom)
print("Ukuran Data:", data.shape)

# Importing necessary libraries
import pandas as pd
import numpy as np

# Data Visualization
from matplotlib import pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# NLP
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from wordcloud import WordCloud, STOPWORDS
import re

# Warning
import warnings
warnings.filterwarnings('ignore')

# Load the data
train_df = pd.read_csv(r"train_E6oV3lV.csv")
print(f'Train data shape: {train_df.shape}')

test_df = pd.read_csv(r"test_tweets_anuFYb8.csv")
print(f'Test data shape: {test_df.shape}')

# Check for duplicates and missing values
print(f'Duplicated entries in train data: {train_df.duplicated().sum()}')
print(f'Missing values in train data:\n{train_df.isnull().sum()}')
print('-' * 40)
print(f'Missing values in test data:\n{test_df.isnull().sum()}')

# Generate word clouds
stopwords = set(STOPWORDS)
stopwords.add('user')

# Negative tweets word cloud
negative_tweets = train_df['tweet'][train_df['label'] == 1].to_string()
wordcloud_negative = WordCloud(width=800, height=800, background_color='white',
                               stopwords=stopwords, min_font_size=10).generate(negative_tweets)

# Positive tweets word cloud
positive_tweets = train_df['tweet'][train_df['label'] == 0].to_string()
wordcloud_positive = WordCloud(width=800, height=800, background_color='white',
                               stopwords=stopwords, min_font_size=10).generate(positive_tweets)

# Plot word clouds
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.imshow(wordcloud_negative)
plt.axis("off")
plt.title('Negative Tweets', fontsize=20)

plt.subplot(1, 2, 2)
plt.imshow(wordcloud_positive)
plt.axis("off")
plt.title('Positive Tweets', fontsize=20)

plt.tight_layout()
plt.show()

# Feature engineering
train_df['tweet_length'] = train_df['tweet'].str.len()
train_df['num_hashtags'] = train_df['tweet'].str.count('#')
train_df['num_exclamation_marks'] = train_df['tweet'].str.count('!')
train_df['num_question_marks'] = train_df['tweet'].str.count('\?')
train_df['total_tags'] = train_df['tweet'].str.count('@')
train_df['num_punctuations'] = train_df['tweet'].str.count('[.,:;]')
train_df['num_words'] = train_df['tweet'].apply(lambda x: len(x.split()))

# Visualize relationships of features with labels
plt.figure(figsize=(12, 16))
features = ['tweet_length', 'num_hashtags', 'num_exclamation_marks', 'num_question_marks',
            'total_tags', 'num_punctuations', 'num_words']
for i, feature in enumerate(features):
    plt.subplot(4, 2, i + 1)
    sns.kdeplot(train_df[train_df['label'] == 0][feature], label='Positive', fill=True)
    sns.kdeplot(train_df[train_df['label'] == 1][feature], label='Negative', fill=True)
    plt.legend()
plt.tight_layout()
plt.show()

#data preprocessing:

# Train-Test Splitting
X = train_df.drop(columns=['label'])
y = train_df['label']
test = test_df
print(X.shape, test.shape, y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=8)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


# Function to tokenize and clean the text
def tokenize_and_clean(text):
    # Changing case of the text to lower case
    lowered = text.lower()

    # Cleaning the text
    cleaned = re.sub('@user', '', lowered)

    # Tokenization
    tokens = word_tokenize(cleaned)
    filtered_tokens = [token for token in tokens if re.match(r'\w{1,}', token)]

    # Stemming
    stemmer = PorterStemmer()
    stems = [stemmer.stem(token) for token in filtered_tokens]
    return stems

# Import NLTK and download necessary resources
import nltk
nltk.download('punkt')
nltk.download('punkt_tab') # Download the missing punkt_tab resource

# BOW Vectorization
bow_vectorizer = CountVectorizer(tokenizer=tokenize_and_clean, stop_words='english')
X_train_tweets_bow = bow_vectorizer.fit_transform(X_train['tweet'])
X_test_tweets_bow = bow_vectorizer.transform(X_test['tweet'])
print(X_train_tweets_bow.shape, X_test_tweets_bow.shape)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words='english')
X_train_tweets_tfidf = tfidf_vectorizer.fit_transform(X_train['tweet'])
X_test_tweets_tfidf = tfidf_vectorizer.transform(X_test['tweet'])
print(X_train_tweets_tfidf.shape, X_test_tweets_tfidf.shape)

# TF-IDF Vectorization on full training data
tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words='english')
X_tweets_tfidf = tfidf_vectorizer.fit_transform(X['tweet'])
test_tweets_tfidf = tfidf_vectorizer.transform(test['tweet'])
print(X_tweets_tfidf.shape, test_tweets_tfidf.shape)


# Class Imbalance Check
plt.pie(y_train.value_counts(),
        labels=['Label 0 (Positive Tweets)', 'Label 1 (Negative Tweets)'],
        autopct='%0.1f%%')
plt.axis('equal')
plt.show()

# SMOTE to deal with the class imbalance
smote = SMOTE()
X_train_smote, y_train_smote = smote.fit_resample(X_train_tweets_tfidf, y_train.values)
print(X_train_smote.shape, y_train_smote.shape)

# SMOTE on full training data
smote = SMOTE()
X_smote, y_smote = smote.fit_resample(X_tweets_tfidf, y.values)
print(X_smote.shape, y_smote.shape)

# Class Imbalance Check
plt.pie(pd.value_counts(y_train_smote),
        labels=['Label 0 (Positive Tweets)', 'Label 1 (Negative Tweets)'],
        autopct='%0.1f%%')
plt.axis('equal')
plt.show()

# Functions to print scores
def training_scores(y_act, y_pred):
    acc = round(accuracy_score(y_act, y_pred), 3)
    f1 = round(f1_score(y_act, y_pred), 3)
    print(f'Training Scores: Accuracy={acc}, F1-Score={f1}')

def validation_scores(y_act, y_pred):
    acc = round(accuracy_score(y_act, y_pred), 3)
    f1 = round(f1_score(y_act, y_pred), 3)
    print(f'Validation Scores: Accuracy={acc}, F1-Score={f1}')

def display_prediction_summary(model_name, y_true, y_pred):
    df = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred})
    print(f"Prediction Results for {model_name}:")
    display(df.head())
    print("\n")

# List to store model names, training scores, and validation scores
model_names = []
training_accuracies = []
training_f1_scores = []
validation_accuracies = []
validation_f1_scores = []

# Function to store scores for visualization
def record_scores(model_name, train_acc, train_f1, val_acc, val_f1):
    model_names.append(model_name)
    training_accuracies.append(train_acc)
    training_f1_scores.append(train_f1)
    validation_accuracies.append(val_acc)
    validation_f1_scores.append(val_f1)

# Logistic Regression
lr = LogisticRegression()
lr.fit(X_train_smote, y_train_smote)
y_train_pred = lr.predict(X_train_smote)
y_test_pred = lr.predict(X_test_tweets_tfidf)
training_scores(y_train_smote, y_train_pred)
validation_scores(y_test, y_test_pred)
display_prediction_summary("Logistic Regression", y_test, y_test_pred)

train_acc, train_f1 = accuracy_score(y_train_smote, y_train_pred), f1_score(y_train_smote, y_train_pred)
val_acc, val_f1 = accuracy_score(y_test, y_test_pred), f1_score(y_test, y_test_pred)

record_scores("Logistic Regression", train_acc, train_f1, val_acc, val_f1)

# Naive Bayes Classifier
mnb = MultinomialNB()
mnb.fit(X_train_smote, y_train_smote)
y_train_pred = mnb.predict(X_train_smote)
y_test_pred = mnb.predict(X_test_tweets_tfidf)
training_scores(y_train_smote, y_train_pred)
validation_scores(y_test, y_test_pred)
display_prediction_summary("Naive Bayes Classifier", y_test, y_test_pred)

train_acc, train_f1 = accuracy_score(y_train_smote, y_train_pred), f1_score(y_train_smote, y_train_pred)
val_acc, val_f1 = accuracy_score(y_test, y_test_pred), f1_score(y_test, y_test_pred)

record_scores("Naive Bayes", train_acc, train_f1, val_acc, val_f1)

# Random Forest Classifier
rf = RandomForestClassifier()
rf.fit(X_train_smote, y_train_smote)
y_train_pred = rf.predict(X_train_smote)
y_test_pred = rf.predict(X_test_tweets_tfidf)
training_scores(y_train_smote, y_train_pred)
validation_scores(y_test, y_test_pred)
display_prediction_summary("Random Forest", y_test, y_test_pred)

# Extreme Gradient Boosting Classifier
xgb = XGBClassifier(objective='binary:logistic', eval_metric='logloss')
xgb.fit(X_train_smote, y_train_smote)
y_train_pred = xgb.predict(X_train_smote)
y_test_pred = xgb.predict(X_test_tweets_tfidf)
training_scores(y_train_smote, y_train_pred)
validation_scores(y_test, y_test_pred)
display_prediction_summary("XGBoosting", y_test, y_test_pred)

#HYPERPARAMETER TUNING
# Random Forest Classifier
rf = RandomForestClassifier(criterion='entropy', max_samples=0.8,
                            min_samples_split=10, random_state=0)
rf.fit(X_train_smote, y_train_smote)
y_train_pred = rf.predict(X_train_smote)
y_test_pred = rf.predict(X_test_tweets_tfidf)
training_scores(y_train_smote, y_train_pred)
validation_scores(y_test, y_test_pred)
display_prediction_summary("Random Forest", y_test, y_test_pred)

train_acc, train_f1 = accuracy_score(y_train_smote, y_train_pred), f1_score(y_train_smote, y_train_pred)
val_acc, val_f1 = accuracy_score(y_test, y_test_pred), f1_score(y_test, y_test_pred)

record_scores("Random Forest", train_acc, train_f1, val_acc, val_f1)

#HYPERPARAMETER TUNING
# Extreme Gradient Boosting Classifier
xgb = XGBClassifier(objective='binary:logistic', eval_metric='logloss',
                    learning_rate=0.8, max_depth=20, gamma=0.6,
                    reg_lambda=0.1, reg_alpha=0.1)
xgb.fit(X_train_smote, y_train_smote)
y_train_pred = xgb.predict(X_train_smote)
y_test_pred = xgb.predict(X_test_tweets_tfidf)
training_scores(y_train_smote, y_train_pred)
validation_scores(y_test, y_test_pred)
display_prediction_summary("XGBoosting", y_test, y_test_pred)

train_acc, train_f1 = accuracy_score(y_train_smote, y_train_pred), f1_score(y_train_smote, y_train_pred)
val_acc, val_f1 = accuracy_score(y_test, y_test_pred), f1_score(y_test, y_test_pred)

record_scores("XGBoosting", train_acc, train_f1, val_acc, val_f1)

# Plotting Results
x = range(len(model_names))
width = 0.35  # Bar width

fig, ax = plt.subplots(figsize=(10, 6))

# Training scores
train_bars = ax.bar([i - width/2 for i in x], training_accuracies, width, label='Training Accuracy', color='skyblue')
train_f1_bars = ax.bar([i - width/2 for i in x], training_f1_scores, width, label='Training F1-Score', color='dodgerblue')

# Validation scores
val_bars = ax.bar([i + width/2 for i in x], validation_accuracies, width, label='Validation Accuracy', color='lightcoral')
val_f1_bars = ax.bar([i + width/2 for i in x], validation_f1_scores, width, label='Validation F1-Score', color='red')

# Labels, Title, and Legend
ax.set_xticks(x)
ax.set_xticklabels(model_names)
ax.set_xlabel("Models")
ax.set_ylabel("Scores")
ax.set_title("Model Performance: Accuracy and F1-Score")
ax.legend(loc='lower right')

# Displaying scores on bars
for bars in [train_bars, train_f1_bars, val_bars, val_f1_bars]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Predicting test data on full training data
rf = RandomForestClassifier(criterion='entropy', max_samples=0.8,
                            min_samples_split=10, random_state=0)
rf.fit(X_smote, y_smote)
predictions = rf.predict(test_tweets_tfidf)
submission = pd.DataFrame({'id':test_df.id,'tweet':test_df.tweet, 'label':predictions})
submission.head()

# @title label

from matplotlib import pyplot as plt
submission['label'].plot(kind='hist', bins=20, title='label')
plt.gca().spines[['top', 'right',]].set_visible(False)

# @title Distribution of Predicted Labels

import matplotlib.pyplot as plt

# Assuming 'submission' is your DataFrame
labels = submission['label'].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(labels, labels=['Positive', 'Negative'], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
plt.title('Distribution of Predicted Labels')
_ = plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

submission.to_csv(r"C:\Users\user\Downloads\test_tweets_anuFYb8.csv", index=False)
print('Submission is successful!')