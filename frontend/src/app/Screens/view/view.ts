import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { Assign } from '../../components/assign/assign';

@Component({
  selector: 'app-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './view.html',
  styleUrl: './view.css',
})
export class View {
  dialog = inject(MatDialog);
  trainingPrograms = [
    {
      name: 'Program Name',
      sessions: [
        {
          name: 'Morning Session',
          time: '09:00 - 10:30',
          capacity: 20,
          participants: ['John', 'Sarah', 'Mike', 'Lebo']
        },
        {
          name: 'Midday Session',
          time: '11:00 - 12:30',
          capacity: 20,
          participants: ['Thabo', 'Aisha']
        },
        {
          name: 'Afternoon Session',
          time: '13:00 - 14:30',
          capacity: 20,
          participants: []
        }
      ]
    }
  ];

  openAssign() {
    this.dialog.open(Assign, {

    });
  }

  getRemainingSeats(session: any): number {
    return session.capacity - session.participants.length;
  }
}