import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { VoiceRecognitionService } from '../../services/voice-recognition.service';

@Component({
  selector: 'app-voice-input',
  templateUrl: './voice-input.component.html',
  styleUrls: ['./voice-input.component.scss']
})
export class VoiceInputComponent implements OnInit {
  @Output() textRecognized = new EventEmitter<string>();
  
  isRecording = false;
  recordingTime = 0;
  timerInterval: any;
  
  constructor(private voiceRecognitionService: VoiceRecognitionService) { }
  
  ngOnInit(): void {
    this.voiceRecognitionService.voiceText$.subscribe(text => {
      if (text) {
        this.textRecognized.emit(text);
      }
    });
  }
  
  toggleRecording(): void {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      this.startRecording();
    }
  }
  
  startRecording(): void {
    this.voiceRecognitionService.start();
    this.isRecording = true;
    this.recordingTime = 0;
    
    // Start timer
    this.timerInterval = setInterval(() => {
      this.recordingTime++;
      
      // Auto-stop after 30 seconds
      if (this.recordingTime >= 30) {
        this.stopRecording();
      }
    }, 1000);
  }
  
  stopRecording(): void {
    this.voiceRecognitionService.stop();
    this.isRecording = false;
    
    // Clear timer
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }
  
  formatTime(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
}