import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MaterialDesignFrameworkModule } from '@ajsf/material';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Bootstrap4FrameworkModule } from '@ajsf/bootstrap4';
import { Bootstrap3FrameworkModule } from '@ajsf/bootstrap3';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    MaterialDesignFrameworkModule,
    HttpClientModule,
    BrowserAnimationsModule,
    Bootstrap4FrameworkModule,
    Bootstrap3FrameworkModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }


