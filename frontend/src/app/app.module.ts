import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatWidgetComponent } from './components/chat-widget/chat-widget.component';
import { MessageItemComponent } from './components/message-item/message-item.component';
import { VoiceInputComponent } from './components/voice-input/voice-input.component';

@NgModule({
  declarations: [
    AppComponent,
    ChatWidgetComponent,
    MessageItemComponent,
    VoiceInputComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }