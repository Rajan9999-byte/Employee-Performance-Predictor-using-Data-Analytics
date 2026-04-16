import subprocess
import sys
import os

def run_pipeline():
    print("--- 🚀 Starting Employee Performance Predictor Pipeline ---")
    
    # 1. Generate Data
    print("\n[Step 1/3] Generating Synthetic HR Data...")
    subprocess.run([sys.executable, "src/generator.py"], check=True)
    
    # 2. Train Model
    print("\n[Step 2/3] Training Machine Learning Model...")
    subprocess.run([sys.executable, "src/train_model.py"], check=True)
    
    # 3. Launch Message
    print("\n[Step 3/3] Pipeline Complete!")
    print("\n" + "="*50)
    print("SUCCESS: Your model and data are ready.")
    print("To launch the interactive dashboard, run:")
    print("streamlit run src/dashboard.py")
    print("="*50)

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\n❌ Error in pipeline: {e}")
