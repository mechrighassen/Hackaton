import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SigninComponent } from './signin/signin.component';
import { IndexComponent } from './index/index.component';
import { AlgorithmComponent } from './algorithm/algorithm.component';
import { AlgorithmNewComponent } from './algorithm-new/algorithm-new.component';

const routes: Routes = [
  { path: 'signin', component: SigninComponent },
  { path: 'index', component: IndexComponent },
  { path: 'algorithm', component: AlgorithmComponent },
  { path: 'algorithm_new', component: AlgorithmNewComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
