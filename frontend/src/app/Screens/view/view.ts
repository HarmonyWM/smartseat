import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './view.html',
  styleUrl: './view.css',
})
export class View {

  // 🔹 Dummy data (safe for now)
  departments = [
    {
      name: 'Division A',
      totalParticipants: 24,
      maxPerSession: 8
    },
    {
      name: 'Division B',
      totalParticipants: 18,
      maxPerSession: 8
    },
    {
      name: 'Division C',
      totalParticipants: 18,
      maxPerSession: 6
    }
  ];

  // 🔹 Business logic
  getRemainingSeats(dept: any): number {
    const totalSessions = 3;
    return (dept.maxPerSession * totalSessions) - dept.totalParticipants;
  }

}