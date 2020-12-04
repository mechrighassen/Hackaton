import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SigninComponent } from './signin/signin.component';
import { IndexComponent } from './index/index.component';
import { AlgorithmComponent } from './algorithm/algorithm.component';
import { AlgorithmNewComponent } from './algorithm-new/algorithm-new.component';

@NgModule({
  declarations: [
    AppComponent,
    SigninComponent,
    IndexComponent,
    AlgorithmComponent,
    AlgorithmNewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
