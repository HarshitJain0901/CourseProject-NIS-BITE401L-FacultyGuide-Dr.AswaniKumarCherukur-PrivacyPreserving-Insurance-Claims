from data_preprocessing import preprocess_data
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
import os

def train_and_save_model():
    X_processed, y = preprocess_data()

    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_processed, y)

    os.makedirs("src", exist_ok=True)
    joblib.dump(model, 'src/model.joblib')

    # Save coefficients as dot product is used in HE (simulate it using mean feature importances)
    # We'll still store intercept = mean_prediction probability for sigmoid approx
    np.save('src/model_coefficients.npy', model.feature_importances_)
    np.save('src/model_intercept.npy', [model.predict_proba(X_processed)[:, 1].mean()])

if __name__ == '__main__':
    train_and_save_model()
