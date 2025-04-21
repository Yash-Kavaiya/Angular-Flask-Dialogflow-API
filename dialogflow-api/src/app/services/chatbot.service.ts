import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DialogflowResponse } from '../models/dialogflow-response.model';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  // URL of our Flask backend
  private apiUrl = 'https://upgraded-spoon-6xxpr69x9vvh4v56-5000.app.github.dev/api/dialogflow';

  constructor(private http: HttpClient) {}

  /**
   * Send a message to Dialogflow through our Flask backend
   * @param message - The user's message to send to Dialogflow
   * @returns An Observable with the Dialogflow response
   */
  sendMessage(message: string): Observable<DialogflowResponse> {
    return this.http.post<DialogflowResponse>(this.apiUrl, { message });
  }
}
