



import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')

# Load dataset
df = pd.read_csv("expensessssss_data_indian_household.csv")

# NLP Preprocessing
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove punctuation and digits
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

df['Cleaned_Description'] = df['Description'].apply(clean_text)

# Features and Labels
X = df['Cleaned_Description']
y = df['Category']

# TF-IDF with n-grams
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1500)
X_tfidf = vectorizer.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Prediction Function
def predict_expense(text):
    text = clean_text(text)
    text_tfidf = vectorizer.transform([text])
    return model.predict(text_tfidf)[0]

# Interaction Loop
print("\nEnhanced Expense Category Predictor")
print("Type a description (e.g. 'bought vegetables', 'paid water bill') or 'exit' to quit\n")

while True:
    user_input = input(">> ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    try:
        prediction = predict_expense(user_input)
        print(f"Predicted Category: {prediction}")
    except:
        print("Sorry, couldn't process that input.")