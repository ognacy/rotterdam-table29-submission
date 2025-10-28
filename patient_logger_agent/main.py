from patient_logger.agent import root_agent
from vertexai.agent_engines import AdkApp

app = AdkApp(agent=root_agent)
