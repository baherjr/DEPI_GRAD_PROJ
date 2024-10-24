import mlflow
import mlflow.pyfunc
import joblib

# Load the pre-trained ARIMA model from the .pkl file
model_fit = joblib.load('arima_model.pkl')

# Start MLflow run
with mlflow.start_run():
    # Log model type parameter
    mlflow.log_param("model_type", "ARIMA")

    # Log the ARIMA model artifact (pkl file)
    mlflow.log_artifact('arima_model.pkl')

    # Log metrics (replace with actual values from your evaluation)
    mse_value = 123  # Replace with the actual MSE or relevant evaluation metric
    mlflow.log_metric("mse", mse_value)

    print("Model logged in MLflow")
