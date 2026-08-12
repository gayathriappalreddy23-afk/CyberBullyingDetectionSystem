import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Define some training data
texts = [
    # Safe texts
    "Hello there! How are you doing today?",
    "I hope you have a wonderful day and succeed in your work.",
    "This is an amazing project and I love the interface design.",
    "Let's collaborate on this task and build something great.",
    "Thank you for sharing this information, it was very helpful.",
    "Congratulations on winning the contest, you deserved it!",
    "I agree with your analysis, it makes complete sense.",
    "Let's meet tomorrow for coffee and talk about it.",
    
    # Cyberbullying texts
    "You are so stupid and ugly, no one wants to talk to you.",
    "I hate you, you are a complete loser and worthless.",
    "Nobody likes you here. You should go away and die.",
    "You are an idiot and your opinions are trash.",
    "Shut up, you dumb jerk. You know nothing.",
    "Go kill yourself, you are a waste of space.",
    "You are extremely ugly and fat, get off this platform."
]

labels = [
    "Safe", "Safe", "Safe", "Safe", "Safe", "Safe", "Safe", "Safe",
    "Cyberbullying", "Cyberbullying", "Cyberbullying", "Cyberbullying", "Cyberbullying", "Cyberbullying", "Cyberbullying"
]

def train():
    print("Fitting Vectorizer and Model...")
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    # Initialize Logistic Regression Classifier
    model = LogisticRegression()
    model.fit(X, labels)
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # Save the vectorizer and model
    with open('model/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
        
    with open('model/cyberbullying_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("Model and vectorizer trained and saved successfully!")

    # Write a simple synthetic CSV to dataset directory so it has contents
    os.makedirs('dataset', exist_ok=True)
    csv_path = 'dataset/cyberbullying_dataset.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("text,label\n")
        for t, l in zip(texts, labels):
            # Escape double quotes
            t_escaped = t.replace('"', '""')
            f.write(f'"{t_escaped}","{l}"\n')
    print("Dataset CSV generated successfully!")

if __name__ == '__main__':
    train()
