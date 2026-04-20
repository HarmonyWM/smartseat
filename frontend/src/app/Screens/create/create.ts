import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './create.html',
  styleUrl: './create.css',
})
export class Create {

  departmentForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.departmentForm = this.fb.group({
      name: ['', Validators.required],
      totalParticipants: [0, [Validators.required, Validators.min(1)]],
      maxPerSession: [0, [Validators.required, Validators.min(1), Validators.max(20)]]
    });
  }

  onSubmit() {
    if (this.departmentForm.invalid) return;

    const dept = this.departmentForm.value;

    //  Business rule validation
    if (dept.maxPerSession > dept.totalParticipants) {
      alert('Max per session cannot exceed total participants');
      return;
    }

    const totalSessions = 3;
    const totalSeats = dept.maxPerSession * totalSessions;

    if (totalSeats < dept.totalParticipants) {
      alert('Not enough seats across sessions for this department');
      return;
    }

    console.log('Department Created:', dept);

  }
}