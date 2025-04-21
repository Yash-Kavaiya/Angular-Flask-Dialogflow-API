/**
 * Represents a message in the chat interface
 */
export interface Message {
  /** Content of the message */
  content: string;
  
  /** Who sent the message ('user' or 'bot') */
  sender: 'user' | 'bot';
  
  /** When the message was sent */
  timestamp: Date;
  
  /** Optional rich response data from Dialogflow */
  richResponse?: any;
}
