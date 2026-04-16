import pandas as pd
import numpy as np
import os

def generate_employee_data(n_employees=1500):
    np.random.seed(42)
    
    # Departments
    departments = ['Engineering', 'Sales', 'HR', 'Marketing', 'Finance', 'Data Science']
    
    # Generate Base Features
    data = {
        'Employee_ID': [f'EMP{1000+i}' for i in range(n_employees)],
        'Department': np.random.choice(departments, n_employees),
        'Age': np.random.randint(22, 60, n_employees),
        'Gender': np.random.choice(['Male', 'Female', 'Non-Binary'], n_employees, p=[0.48, 0.48, 0.04]),
        'Years_At_Company': np.random.randint(1, 15, n_employees),
        'Job_Level': np.random.randint(1, 6, n_employees),
        'Weekly_Hours': np.random.randint(35, 60, n_employees),
        'Training_Hours': np.random.randint(10, 100, n_employees),
        'Projects_Completed': np.random.randint(1, 10, n_employees),
        'Attendance_Rate': np.random.uniform(0.8, 1.0, n_employees),
        'Engagement_Score': np.random.uniform(1, 5, n_employees),
        'Salary_Hike_Pct': np.random.randint(5, 25, n_employees)
    }
    
    df = pd.DataFrame(data)
    
    # Simulate Previous Cycle Performance (Cycle -1 and Cycle -2)
    # Most people stay consistent, some improve, some decline
    df['Prev_Rating_1'] = np.random.choice([0, 1, 2], n_employees, p=[0.2, 0.6, 0.2]) # Low, Med, High
    df['Prev_Rating_2'] = np.random.choice([0, 1, 2], n_employees, p=[0.15, 0.7, 0.15])
    
    # Logic for current score based on historical trend
    def calculate_performance(row):
        # Base score from current metrics
        score = (
            (row['Projects_Completed'] * 0.5) +
            (row['Training_Hours'] / 10 * 0.3) +
            (row['Engagement_Score'] * 0.5) +
            (row['Attendance_Rate'] * 10 * 0.2) +
            (row['Job_Level'] * 0.2) +
            (row['Prev_Rating_1'] * 0.4) # Consistency factor
        )
        
        # Noise
        score += np.random.normal(0, 0.4)
        
        if score > 10.5:
            return 'High'
        elif score > 6.5:
            return 'Medium'
        else:
            return 'Low'
            
    df['Performance_Score'] = df.apply(calculate_performance, axis=1)
    
    # Attrition Risk Simulation (Burnout or Low Engagement)
    def calculate_attrition(row):
        risk = 0
        if row['Weekly_Hours'] > 55: risk += 0.4 # Burnout
        if row['Engagement_Score'] < 2.0: risk += 0.4 # Disengaged
        if row['Performance_Score'] == 'Low': risk += 0.2 # Poor performance
        
        risk += np.random.normal(0, 0.1)
        return min(max(risk, 0), 1)
        
    df['Attrition_Risk'] = df.apply(calculate_attrition, axis=1)
    
    return df

if __name__ == "__main__":
    df = generate_employee_data()
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    output_path = os.path.join('data', 'employee_performance.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Enhanced dataset generated with {len(df)} records!")
    print(df['Performance_Score'].value_counts())
