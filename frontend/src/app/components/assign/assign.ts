import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { form, FormField } from '@angular/forms/signals';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { divisions, sessions } from '../../utils/Hard-coded';
import { assignment } from '../../utils/interface/assignment';
import { Data } from '../../Services/data.service';

@Component({
  selector: 'app-assign',
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatAutocompleteModule,
    MatButtonModule,
    FormField
],
  templateUrl: './assign.html',
  styleUrl: './assign.css',
})
export class Assign implements OnInit {
  selectDepartment!: any;
  ngOnInit(): void {
    this.dataServices.get('/programs').subscribe({
      next: (res: any) => {
        this.programs.update(() => res);
        console.log(res);
      },
      error: (err: any) => {
        console.log(err.error);
      },
    });
  }
  dialogRef = inject(MatDialogRef<Assign>);
  dataServices = inject(Data);

  assignment = signal<assignment>({
    participant_Id: "",
    session_Id: ""
  }); // Adding assignment to session
  participants = signal<any[]>([]); // List of Participants filtered by Division
  divisions = signal<any[]>(divisions); // Get list of divisions
  sessions = signal<any[]>(sessions); // Get static sessions
  programs = signal<any[]>([]); // Get list of avaliable programs
  participantsDisabled = signal<boolean>(true);

  assignmentForm = form(this.assignment, {});

  openParticipants() {
    this.dataServices.get('/participants').subscribe({
      next: (res: any) => {
        this.participants.update(() =>
          (res as any[]).filter((a: any) => a.department == this.selectDepartment),
        );
        this.participantsDisabled.update(() => false);
        console.log(res);
      },
      error: (err: any) => {
        console.log(err.error);
      },
    });
  }

  onClose() {
    this.dialogRef.close();
  }

  onSubmit() {
    this.dataServices.post('/allocate', this.assignment()).subscribe({
      next: (res: any) => {
        console.log(res);
        this.onClose();
      },
      error: (err: any) => {
        console.log(err.error);
      },
    });
  }
}
