import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import os
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/ram/Pravah/pravah-template")
DATASET_PATH = BASE_DIR / "navi_mumbai_real_estate_uncleaned_2500_cleaned.csv"
OUTPUT_DIR = Path("/Users/ram/Pravah/backend/app/model")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_SAVE_PATH = OUTPUT_DIR / "model_v2.pkl"

def clean_data(df):
    """
    Clean the dataset:
    1. Remove rows with negative values in key columns.
    2. Handle outliers.
    3. Ensure data types are correct.
    """
    print(f"Original shape: {df.shape}")
    
    # Remove negative values
    cols_to_check = ['area_sqft', 'actual_price', 'floor', 'total_floors']
    for col in cols_to_check:
        df = df[df[col] >= 0]
    
    # Remove obvious outliers in area (e.g., > 10000 sqft for a regular house)
    df = df[df['area_sqft'] < 10000]
    
    # Ensure bhk and bathrooms are reasonable
    df = df[(df['bhk'] > 0) & (df['bhk'] < 10)]
    df = df[(df['bathrooms'] > 0) & (df['bathrooms'] < 10)]
    
    print(f"Cleaned shape: {df.shape}")
    return df

def train_and_save():
    # Load
    df = pd.read_csv(DATASET_PATH)
    
    # Clean
    df = clean_data(df)
    
    # Prepare features
    # Drop columns that might not be useful or are redundant
    # floor/total_floors can be kept. age_of_property is good.
    # parking and lift are binary.
    
    # One-hot encode location
    df_encoded = pd.get_dummies(df, columns=['location'], prefix='Location')
    location_columns = [col for col in df_encoded.columns if col.startswith('Location_')]
    
    # Features and target
    X = df_encoded.drop('actual_price', axis=1)
    y = df_encoded['actual_price']
    
    feature_columns = X.columns.tolist()
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"MAE: {mae:,.2f}")
    print(f"RMSE: {rmse:,.2f}")
    print(f"R2 Score: {r2:.4f}")
    
    # Market statistics for the backend logic
    market_stats = {
        'avg_price': df['actual_price'].mean(),
        'avg_price_per_sqft': (df['actual_price'] / df['area_sqft']).mean()
    }
    
    # Save artifacts
    artifacts = {
        'model': model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'location_columns': location_columns,
        'market_stats': market_stats
    }
    
    with open(MODEL_SAVE_PATH, 'wb') as f:
        pickle.dump(artifacts, f)
    
    print(f"Model and artifacts saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_and_save()
