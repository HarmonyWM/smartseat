import { inject, Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root',
})
export class SnackBar {
  snackbar = inject(MatSnackBar);

  openSuccess(message: string) {
    this.snackbar.open(message, 'close', { panelClass: ['success-bar'] });
  }

  openError(message: string) {
    this.snackbar.open(message, 'close', { panelClass: ['error-bar'] });
  }

  openWarning(message: string) {
    this.snackbar.open(message, 'close', { panelClass: ['warn-bar'] });
  }
}
