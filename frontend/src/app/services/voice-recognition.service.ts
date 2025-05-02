import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

interface Window {
  webkitSpeechRecognition: any;
  SpeechRecognition: any;
}

@Injectable({
  providedIn: 'root'
})
export class VoiceRecognitionService {
  recognition: any;
  isRecording = false;
  private voiceTextSubject = new BehaviorSubject<string>('');
  public voiceText$ = this.voiceTextSubject.asObservable();
  
  constructor() {
    this.initRecognition();
  }
  
  initRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const windowObj = window as unknown as Window;
      this.recognition = new (windowObj.SpeechRecognition || windowObj.webkitSpeechRecognition)();
      this.recognition.continuous = false;
      this.recognition.lang = 'en-US';
      this.recognition.maxAlternatives = 1;
      
      this.recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        this.voiceTextSubject.next(transcript);
      };
      
      this.recognition.onerror = (event: any) => {
        console.error('Speech recognition error', event.error);
        this.isRecording = false;
      };
      
      this.recognition.onend = () => {
        this.isRecording = false;
      };
    }
  }
  
  start() {
    if (this.recognition) {
      this.recognition.start();
      this.isRecording = true;
      this.voiceTextSubject.next('');
    } else {
      console.error('Speech recognition not supported in this browser.');
    }
  }
  
  stop() {
    if (this.recognition) {
      this.recognition.stop();
      this.isRecording = false;
    }
  }
}