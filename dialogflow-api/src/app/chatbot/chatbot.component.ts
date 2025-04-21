import { Component, OnInit } from '@angular/core';
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

  constructor(private chatbotService: ChatbotService) {}

  ngOnInit(): void {
    // Add a welcome message from the bot
    this.messages.push({
      content: 'Hello! How can I help you today?',
      sender: 'bot',
      timestamp: new Date()
    });
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
      },
      error: (error) => {
        console.error('Error sending message:', error);
        this.messages.push({
          content: 'Sorry, there was an error processing your request. Please try again.',
          sender: 'bot',
          timestamp: new Date()
        });
        this.loading = false;
      }
    });
  }
}
