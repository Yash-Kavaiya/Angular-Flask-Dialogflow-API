import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { Message } from '../models/message.model';
import { environment } from '../../environments/environment';
import { v4 as uuidv4 } from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = environment.apiUrl;
  private sessionId = uuidv4();
  
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  public messages$ = this.messagesSubject.asObservable();
  
  constructor(private http: HttpClient) { }
  
  getMessages(): Message[] {
    return this.messagesSubject.value;
  }
  
  addMessage(message: Message): void {
    const currentMessages = this.messagesSubject.value;
    this.messagesSubject.next([...currentMessages, message]);
  }
  
  sendMessage(content: string, attachment?: any): Observable<any> {
    const payload: any = {
      message: content,
      session_id: this.sessionId
    };
    
    if (attachment) {
      payload.attachment = attachment;
    }
    
    return this.http.post(`${this.apiUrl}/chat`, payload);
  }
  
  clearMessages(): void {
    this.messagesSubject.next([]);
  }
}