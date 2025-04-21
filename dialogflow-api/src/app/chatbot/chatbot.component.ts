import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChatbotService } from '../services/chatbot.service';
import { Message } from '../models/message.model';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit {
  messages: Message[] = [];
  messageInput = new FormControl('');
  loading = false;
  isChatOpen = false;
  isRecording = false;
  @ViewChild('fileInput') fileInput!: ElementRef;
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  private recognition: any;

  constructor(private chatbotService: ChatbotService) {}

  ngOnInit(): void {
    // Initialize Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      this.initSpeechRecognition();
    }
  }

  initSpeechRecognition(): void {
    // @ts-ignore: Web Speech API types
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    this.recognition.lang = 'en-US'; // Set language

    this.recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      this.messageInput.setValue(transcript);
    };

    this.recognition.onend = () => {
      this.isRecording = false;
    };

    this.recognition.onerror = (event: any) => {
      console.error('Speech recognition error', event.error);
      this.isRecording = false;
    };
  }

  toggleChat(): void {
    this.isChatOpen = !this.isChatOpen;
    if (this.isChatOpen) {
      // Add a welcome message when chat is opened for the first time
      if (this.messages.length === 0) {
        this.messages.push({
          content: 'Hello! How can I help you today?',
          sender: 'bot',
          timestamp: new Date()
        });
      }
      setTimeout(() => this.scrollToBottom(), 100);
    }
  }

  toggleVoiceInput(): void {
    if (!this.recognition) {
      alert('Speech recognition is not supported by your browser.');
      return;
    }

    if (this.isRecording) {
      this.recognition.stop();
    } else {
      this.isRecording = true;
      this.recognition.start();
    }
  }

  openFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    // Here you'd normally process the file and send it to the backend
    // For now, we'll just add a message with the file name
    
    const fileMessage = `I'm sending the file: ${file.name}`;
    this.messageInput.setValue(fileMessage);
    
    // Reset the file input
    input.value = '';
  }

  sendMessage(): void {
    const userMessage = this.messageInput.value?.trim();
    if (!userMessage) return;

    // Add user message to the chat
    this.messages.push({
      content: userMessage,
      sender: 'user',
      timestamp: new Date()
    });

    this.messageInput.setValue('');
    this.loading = true;
    this.scrollToBottom();

    // Send message to Dialogflow via our Flask backend
    this.chatbotService.sendMessage(userMessage).subscribe({
      next: (response) => {
        // Add bot response to the chat
        this.messages.push({
          content: response.response,
          sender: 'bot',
          timestamp: new Date(),
          richResponse: response.rich_response
        });
        this.loading = false;
        this.scrollToBottom();
      },
      error: (error) => {
        console.error('Error sending message:', error);
        this.messages.push({
          content: 'Sorry, there was an error processing your request. Please try again.',
          sender: 'bot',
          timestamp: new Date()
        });
        this.loading = false;
        this.scrollToBottom();
      }
    });
  }

  scrollToBottom(): void {
    if (this.messagesContainer) {
      const element = this.messagesContainer.nativeElement;
      element.scrollTop = element.scrollHeight;
    }
  }
}
