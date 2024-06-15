import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';

@NgModule({
  declarations: [HomeComponent],
  providers: [],
  imports: [CommonModule, RouterModule],
  exports: [],
})
export class FeaturesModule {}
