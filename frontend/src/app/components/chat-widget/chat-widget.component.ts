import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { FileUploadService } from '../../services/file-upload.service';
import { VoiceRecognitionService } from '../../services/voice-recognition.service';
import { Message } from '../../models/message.model';
import { Attachment } from '../../models/attachment.model';
import { v4 as uuidv4 } from 'uuid';

@Component({
  selector: 'app-chat-widget',
  templateUrl: './chat-widget.component.html',
  styleUrls: ['./chat-widget.component.scss']
})
export class ChatWidgetComponent implements OnInit, AfterViewChecked {
  @ViewChild('chatContainer') private chatContainer!: ElementRef;
  
  messages: Message[] = [];
  userInput = '';
  isWidgetOpen = false;
  isRecording = false;
  isSending = false;
  currentAttachment: Attachment | null = null;
  
  constructor(
    private chatService: ChatService,
    private fileUploadService: FileUploadService,
    private voiceRecognitionService: VoiceRecognitionService
  ) { }
  
  ngOnInit(): void {
    // Subscribe to messages from the chat service
    this.chatService.messages$.subscribe(messages => {
      this.messages = messages;
    });
    
    // Subscribe to voice recognition results
    this.voiceRecognitionService.voiceText$.subscribe(text => {
      if (text) {
        this.userInput = text;
      }
    });
    
    // Add initial bot message
    this.addBotMessage('Hello! How can I assist you today?');
  }
  
  ngAfterViewChecked() {
    this.scrollToBottom();
  }
  
  toggleWidget(): void {
    this.isWidgetOpen = !this.isWidgetOpen;
  }
  
  sendMessage(): void {
    if (!this.userInput.trim() && !this.currentAttachment) {
      return;
    }
    
    // Add user message to the chat
    const userMessage: Message = {
      id: uuidv4(),
      content: this.userInput,
      timestamp: new Date(),
      isUser: true,
      attachment: this.currentAttachment || undefined
    };
    
    this.chatService.addMessage(userMessage);
    
    // Show processing indicator
    const processingMessage: Message = {
      id: uuidv4(),
      content: '',
      timestamp: new Date(),
      isUser: false,
      isProcessing: true
    };
    
    this.chatService.addMessage(processingMessage);
    this.isSending = true;
    
    // Send the message to the backend
    this.chatService.sendMessage(this.userInput, this.currentAttachment)
      .subscribe({
        next: (response) => {
          // Remove the processing message
          this.messages = this.messages.filter(m => !m.isProcessing);
          
          // Add bot response
          this.addBotMessage(response.response);
          this.isSending = false;
        },
        error: (error) => {
          console.error('Error sending message', error);
          // Remove the processing message
          this.messages = this.messages.filter(m => !m.isProcessing);
          
          // Add error message
          this.addBotMessage('Sorry, there was an error processing your request.');
          this.isSending = false;
        }
      });
    
    // Clear input and attachment
    this.userInput = '';
    this.currentAttachment = null;
  }
  
  addBotMessage(content: string): void {
    const botMessage: Message = {
      id: uuidv4(),
      content: content,
      timestamp: new Date(),
      isUser: false
    };
    
    this.chatService.addMessage(botMessage);
  }
  
  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      
      // Create attachment object
      this.currentAttachment = {
        name: file.name,
        type: file.type,
        size: file.size
      };
      
      // Upload the file
      this.fileUploadService.uploadFile(file)
        .subscribe({
          next: (response) => {
            if (this.currentAttachment) {
              this.currentAttachment.url = response.url;
            }
          },
          error: (error) => {
            console.error('Error uploading file', error);
            this.currentAttachment = null;
          }
        });
    }
  }
  
  removeAttachment(): void {
    this.currentAttachment = null;
  }
  
  toggleVoiceRecording(): void {
    if (this.isRecording) {
      this.voiceRecognitionService.stop();
    } else {
      this.voiceRecognitionService.start();
    }
    
    this.isRecording = this.voiceRecognitionService.isRecording;
  }
  
  scrollToBottom(): void {
    try {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Error scrolling to bottom', err);
    }
  }
}