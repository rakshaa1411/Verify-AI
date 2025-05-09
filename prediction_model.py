from nltk.corpus import stopwords
import joblib
import nltk
import re
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
nltk.data.path.append('./nltk_data')

# Load updated model and vectorizer
model = joblib.load('model2.pkl')
print('=> Pickle Loaded: Model')
tfidfvect = joblib.load('tfidfvect2.pkl')
print('=> Pickle Loaded: Vectorizer')

class PredictionModel:
    output = {}

    def __init__(self, original_text):
        self.output['original'] = original_text

    def predict(self):
        review = self.preprocess()
        text_vect = tfidfvect.transform([review]).toarray()
        self.output['prediction'] = 'FAKE' if model.predict(text_vect) == 0 else 'REAL'
        return self.output

    def preprocess(self):
        review = re.sub('[^a-zA-Z]', ' ', self.output['original'])
        review = review.lower()
        review = review.split()
        review = [ps.stem(word) for word in review if word not in stopwords.words('english')]
        review = ' '.join(review)
        self.output['preprocessed'] = review
        return review
