import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { form } from '@angular/forms/signals';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-assign',
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatAutocompleteModule,
    MatButtonModule
  ],
  templateUrl: './assign.html',
  styleUrl: './assign.css',
})
export class Assign {
  dialogRef = inject(MatDialogRef<Assign>);

  assignment = signal<any>({}); // Adding assignment to session
  participants = signal<any[]>([]); // List of Participants filtered by Division
  divisions = signal<any[]>([]); // Get list of divisions
  programs = signal<any[]>([]); // Get list of avaliable programs

  assignmentForm = form(this.assignment(), {});

  onClose() {
    this.dialogRef.close();
  }
  
  onSubmit() {}
}
