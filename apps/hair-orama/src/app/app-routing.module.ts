import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      //preloadingStrategy: PreloadAllModules,
      onSameUrlNavigation: 'reload',
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
