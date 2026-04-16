import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from preprocess import preprocess_data

def train_model():
    # 1. Load Preprocessed Data
    print("Loading and preprocessing data...")
    X_train, X_test, y_train, y_test, feature_names = preprocess_data('data/employee_performance.csv')
    
    # 2. Initialize Model
    # Using Random Forest as it provides feature importance and handles non-linear data well
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    # 3. Predictions
    y_pred = model.predict(X_test)
    
    # 4. Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low', 'Medium', 'High']))
    
    # 5. Feature Importance
    importances = model.feature_importances_
    feat_importances = pd.Series(importances, index=feature_names)
    
    plt.figure(figsize=(10, 6))
    feat_importances.nlargest(10).plot(kind='barh', color='skyblue')
    plt.title('Top 10 Drivers of Employee Performance')
    plt.tight_layout()
    
    # Ensure images folder exists
    if not os.path.exists('images'):
        os.makedirs('images')
    plt.savefig('images/feature_importance.png')
    print("Feature importance plot saved to images/feature_importance.png")
    
    # 6. Save Model
    joblib.dump(model, 'models/performance_model.pkl')
    print("Model saved to models/performance_model.pkl")
    
    return model

if __name__ == "__main__":
    train_model()
