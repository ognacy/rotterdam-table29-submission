import vertexai
from vertexai.preview import reasoning_engines

# TODO: Replace with your project ID
PROJECT_ID = "qwiklabs-gcp-04-b310107eab82"
LOCATION = "us-central1"

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# List available reasoning engines
print("Fetching available agents...")
agents = reasoning_engines.ReasoningEngine.list()

if not agents:
    print("No agents found in this project and location.")
else:
    print("Available agents:")
    for i, agent in enumerate(agents):
        print(f"{i + 1}: {agent.display_name} ({agent.resource_name})")

    try:
        selection = int(input("Select an agent by number: "))
        if 1 <= selection <= len(agents):
            selected_agent = agents[selection - 1]
            AGENT_RESOURCE_NAME = selected_agent.resource_name

            # Get the deployed agent
            print("Getting the deployed agent...")
            reasoning_engine = reasoning_engines.ReasoningEngine(AGENT_RESOURCE_NAME)
            print("Agent loaded.")
            print(reasoning_engine.operation_schemas)

            # Start the interaction loop
            while True:
                try:
                    query = input("You: ")
                    if query.lower() == "exit":
                        print("Exiting chat.")
                        break
                except KeyboardInterrupt:
                    print("\nExiting chat.")
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")
