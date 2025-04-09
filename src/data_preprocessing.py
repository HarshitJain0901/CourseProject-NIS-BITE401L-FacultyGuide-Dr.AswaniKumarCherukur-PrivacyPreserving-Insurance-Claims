import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def preprocess_data():
    data = pd.read_csv('data/Insurance.csv')

    # Define target and features (include 'charges' now)
    X = data.drop('insuranceclaim', axis=1)
    y = data['insuranceclaim']

    categorical_features = ['region']
    numerical_features = ['age', 'sex', 'bmi', 'children', 'smoker', 'charges']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])

    # Create a pipeline with preprocessing
    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

    # Fit-transform and save pipeline
    X_processed = pipeline.fit_transform(X)

    os.makedirs("src", exist_ok=True)
    joblib.dump(pipeline, 'src/preprocessor.joblib')

    return X_processed, y

if __name__ == '__main__':
    preprocess_data()
