import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { form } from '@angular/forms/signals';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { divisions, mockParticipants, programs, sessions } from '../../utils/Hard-coded';
import { assignment } from '../../utils/interface/assignment';
import { Data } from '../../Services/data.service';
import { SnackBar } from '../../Services/snack-bar.service';

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
export class Assign implements OnInit {
  selectDepartment!: any;
  selectedProgram: any;
  selectedParticipant: any;
  selectedSession: any;
  ngOnInit(): void {}
  dialogRef = inject(MatDialogRef<Assign>);
  dataServices = inject(Data);
  snackService = inject(SnackBar);

  assignment = signal<assignment>({
    participant_Id: "",
    session_Id: ""
  }); // Adding assignment to session
  participants = signal<any[]>([]); // List of Participants filtered by Division
  divisions = signal<any[]>(divisions); // Get list of divisions
  sessions = signal<any[]>(sessions); // Get static sessions
  allPrograms = programs;
  programs = signal<any[]>([]);
  participantsDisabled = signal<boolean>(true);
  errorMessage = signal<string>('');

  assignmentForm = form(this.assignment, {});

  displayParticipant = (p: any) => p?.name ?? '';

  openParticipants() {
    this.selectedProgram = programs.find((p) => p.department === this.selectDepartment) ?? null;
    this.programs.update(() => this.selectedProgram ? [this.selectedProgram] : []);
    this.dataServices.get('/participants').subscribe({
      next: (res: any) => {
        this.participants.update(() =>
          (res as any[]).filter((a: any) => a.department == this.selectDepartment),
        );
        this.participantsDisabled.update(() => false);
      },
      error: () => {
        const filtered = mockParticipants.filter((p) => p.department === this.selectDepartment);
        this.participants.update(() => filtered);
        this.participantsDisabled.update(() => false);
      },
    });
  }

  onClose() {
    this.dialogRef.close();
  }

  onSubmit() {
    this.errorMessage.set('');
    const payload = {
      participant_id: this.selectedParticipant?.id,
      session_id: this.selectedSession,
    };
    this.dataServices.post('/allocate', payload).subscribe({
      next: (res: any) => {
        console.log(res);
        this.onClose();
      },
      error: (err: any) => {
        this.errorMessage.set(err.error?.error ?? 'Allocation failed. Please try again.');
      },
    });
  }
}
