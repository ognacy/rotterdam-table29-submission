import vertexai
from vertexai import agent_engines
from main import app  # Assuming 'app' is your AdkApp instance in main.py

# Initialize Vertex AI SDK
vertexai.init(project="qwiklabs-gcp-04-b310107eab82", staging_bucket="gs://patient_logs_deploy_staging")

# Define the Python dependencies for the agent
requirements = [
    "google-cloud-aiplatform[agent_engines,adk]",
    "google-cloud-datastore>=2.5.0",
    "pydantic",
    "cloudpickle",
]

# Deploy the agent to Agent Engine
print("Deploying agent to Agent Engine...")
remote_agent = agent_engines.create(
    agent_engine=app,
    requirements=requirements,
    display_name="PatientLoggerAgent",
    extra_packages=["./patient_logger"],
)

print(f"Agent deployed successfully: {remote_agent.name}")
