export interface Message {
  id: string;
  content: string;
  timestamp: Date;
  isUser: boolean;
  attachment?: Attachment;
  isProcessing?: boolean;
}