import vertexai

# TODO: Replace with your project ID and agent resource name
PROJECT_ID = "qwiklabs-gcp-04-b310107eab82"
LOCATION = "us-central1"
AGENT_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/3410478361175130112"

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create a client
client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

# Get the deployed agent
print("Getting the deployed agent...")
agent_engine = client.agent_engines.get(name=AGENT_RESOURCE_NAME)
print("Agent loaded.")
print(dir(agent_engine))

# Start the interaction loop
while True:
    try:
        query = input("You: ")
        if query.lower() == "exit":
            print("Exiting chat.")
            break

        response = agent_engine.query(query)
        print(f"Agent: {response}")

    except KeyboardInterrupt:
        print("\nExiting chat.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")

