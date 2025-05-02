import os
import google.auth
from google.cloud.dialogflowcx_v3.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session as session_pb2

class DialogflowService:
    def __init__(self, project_id, location, agent_id):
        self.project_id = project_id
        self.location = location
        self.agent_id = agent_id
        self.session_client = SessionsClient()
        self.agent_path = f"projects/{project_id}/locations/{location}/agents/{agent_id}"
        
    def detect_intent(self, session_id, text, language_code="en-US"):
        """Returns the result of detect intent with text as input."""
        session_path = f"{self.agent_path}/sessions/{session_id}"
        
        text_input = session_pb2.TextInput(text=text)
        query_input = session_pb2.QueryInput(text=text_input, language_code=language_code)
        request = session_pb2.DetectIntentRequest(
            session=session_path,
            query_input=query_input
        )
        
        response = self.session_client.detect_intent(request=request)
        return response

    def process_dialogflow_response(self, df_response):
        """Process the response from Dialogflow and extract relevant information."""
        query_result = df_response.query_result
        
        # Extract the response text
        response_text = ""
        for message in query_result.response_messages:
            if message.HasField("text"):
                for text in message.text.text:
                    response_text += text + " "
        
        # Extract any payload data (for rich responses like buttons, cards)
        payload = None
        for message in query_result.response_messages:
            if message.HasField("payload"):
                payload = message.payload
        
        return {
            "text": response_text.strip(),
            "intent": query_result.intent.display_name if query_result.intent else None,
            "confidence": query_result.intent_detection_confidence,
            "payload": payload
        }