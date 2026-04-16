import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    # Drop Employee_ID
    df = df.drop('Employee_ID', axis=1)
    
    # Label Encoders
    le_dept = LabelEncoder()
    df['Department'] = le_dept.fit_transform(df['Department'])
    
    le_gender = LabelEncoder()
    df['Gender'] = le_gender.fit_transform(df['Gender'])
    
    # Target Mapping
    target_map = {'Low': 0, 'Medium': 1, 'High': 2}
    df['Performance_Score'] = df['Performance_Score'].map(target_map)
    
    # Features (Including History and Attrition Risk as provided by engine for simulation)
    # In a real case, Attrition_Risk would be another target, but here we use it for dashboard analysis
    # We will exclude it from X features to avoid leaking labels if it's derived from target
    X = df.drop(['Performance_Score', 'Attrition_Risk'], axis=1)
    y = df['Performance_Score']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    if not os.path.exists('models'):
        os.makedirs('models')
        
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(le_dept, 'models/le_dept.pkl')
    joblib.dump(le_gender, 'models/le_gender.pkl')
    
    return X_train_scaled, X_test_scaled, y_train, y_test, X.columns

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, cols = preprocess_data('data/employee_performance.csv')
    print("Preprocessed with enhanced features!")
    print(f"Features included: {list(cols)}")
