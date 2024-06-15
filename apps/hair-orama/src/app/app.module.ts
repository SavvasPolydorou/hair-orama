import { ViewportScroller } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Router, RouterModule, Scroll } from '@angular/router';
import { filter } from 'rxjs';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FeaturesModule } from './features/features.module';

@NgModule({
  declarations: [],
  imports: [
    BrowserModule.withServerTransition({ appId: 'serverApp' }),
    AppComponent,
    HttpClientModule,
    AppRoutingModule,
    FeaturesModule,
    BrowserAnimationsModule,
    RouterModule,
  ],
  exports: [],
  providers: [
    provideClientHydration(),
    //{ provide: HTTP_INTERCEPTORS, useClass: RetryInterceptor, multi: true },
  ],
  //bootstrap: [AppComponent],
})
export class AppModule {
  constructor(router: Router, viewportScroller: ViewportScroller) {
    router.events.pipe(filter(e => e instanceof Scroll)).subscribe((e: any) => {
      if (e.anchor) {
        // anchor navigation
        /* setTimeout is the core line to solve the solution */
        const el = document.getElementById(e.anchor);
        setTimeout(() => {
          return el?.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            inline: 'start',
          });
        });
      } else if (e?.position) {
        // backward navigation
        viewportScroller.scrollToPosition(e?.position);
      } else {
        // forward navigation
        viewportScroller.scrollToPosition([0, 0]);
      }
    });
  }
}
