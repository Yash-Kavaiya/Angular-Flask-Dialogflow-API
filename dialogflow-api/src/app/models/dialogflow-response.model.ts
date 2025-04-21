/**
 * Represents a response from the Dialogflow API
 */
export interface DialogflowResponse {
  /** The text response from Dialogflow */
  response: string;
  
  /** The detected intent name */
  intent: string;
  
  /** Confidence score for the intent detection */
  confidence: number;
  
  /** Optional rich response data (buttons, cards, etc.) */
  rich_response?: any;
}
