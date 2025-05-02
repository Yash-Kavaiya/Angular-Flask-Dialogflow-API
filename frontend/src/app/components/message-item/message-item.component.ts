import { Component, Input } from '@angular/core';
import { Message } from '../../models/message.model';

@Component({
  selector: 'app-message-item',
  templateUrl: './message-item.component.html',
  styleUrls: ['./message-item.component.scss']
})
export class MessageItemComponent {
  @Input() message!: Message;
  
  getFileIconClass(mimeType: string): string {
    if (mimeType.startsWith('image/')) {
      return 'fa-file-image';
    } else if (mimeType.startsWith('application/pdf')) {
      return 'fa-file-pdf';
    } else if (mimeType.includes('document') || mimeType.includes('word')) {
      return 'fa-file-word';
    } else if (mimeType.includes('sheet') || mimeType.includes('excel')) {
      return 'fa-file-excel';
    } else if (mimeType.startsWith('text/')) {
      return 'fa-file-alt';
    } else {
      return 'fa-file';
    }
  }
  
  formatTimestamp(timestamp: Date): string {
    const now = new Date();
    const messageDate = new Date(timestamp);
    
    // If the message is from today, just show the time
    if (messageDate.toDateString() === now.toDateString()) {
      return messageDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Otherwise, show the date and time
    return messageDate.toLocaleString([], {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
}