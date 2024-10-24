from azureml.core import Workspace, Model, Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice  # for ACI deployment
from azureml.core.webservice import AksWebservice  # for AKS deployment
from azureml.core.conda_dependencies import CondaDependencies

# Connect to your existing workspace
ws = Workspace.from_config()  # This will use the config.json in your directory
# Or specify directly:
# ws = Workspace.get(name='your-workspace-name',
#                   subscription_id='your-subscription-id',
#                   resource_group='your-resource-group')

# Register the model
model = Model.register(workspace=ws,
                      model_path='./model.pkl',  # local path to model
                      model_name='your-model-name',
                      description='Your model description')

# Create environment
env = Environment('model-env')
conda_dep = CondaDependencies()

# Add required packages based on your model type
# For scikit-learn:
conda_dep.add_conda_package('scikit-learn')
# For PyTorch:
# conda_dep.add_conda_package('pytorch')
# For TensorFlow:
# conda_dep.add_conda_package('tensorflow')

conda_dep.add_pip_package('azureml-defaults')
env.python.conda_dependencies = conda_dep

# Create scoring script
%%writefile score.py
import json
import pickle
import numpy as np
from azureml.core.model import Model

def init():
    global model
    model_path = Model.get_model_path('your-model-name')
    model = pickle.load(open(model_path, 'rb'))

def run(raw_data):
    try:
        data = json.loads(raw_data)
        data = np.array(data['data'])
        result = model.predict(data)
        return json.dumps({"prediction": result.tolist()})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Set up inference config
inference_config = InferenceConfig(
    entry_script="score.py",
    environment=env
)

# Deploy to ACI (for development/testing)
aci_config = AciWebservice.deploy_configuration(
    cpu_cores=1,
    memory_gb=1,
    auth_enabled=True,
    enable_app_insights=True,
    tags={'environment': 'dev'}
)

service = Model.deploy(
    workspace=ws,
    name='your-service-name',
    models=[model],
    inference_config=inference_config,
    deployment_config=aci_config
)

service.wait_for_deployment(show_output=True)

# Get the scoring URL and key
print(f'Scoring URL: {service.scoring_uri}')
print(f'Primary key: {service.get_keys()[0]}')

# Test the deployed service
import requests

# Sample data for testing
test_data = {
    "data": [[1.0, 2.0, 3.0, 4.0]]  # Adjust based on your model's input requirements
}

# Make prediction
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {service.get_keys()[0]}'
}

response = requests.post(service.scoring_uri, json=test_data, headers=headers)
print(response.json())