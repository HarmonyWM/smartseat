import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Participant {
  id: number;
  name: string;
  department: 'A' | 'B' | 'C';
  assignedSession?: string;
}

export interface Session {
  id: string;
  name: string;
  time: string;
  capacity: number;
  participants: Participant[];
  departmentLimits: {
    A: number;
    B: number;
    C: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class TrainingService {

  private apiUrl = 'https://your-api-url'; // going to replace layer 

  constructor(private http: HttpClient) {}

  // GET all sessions
  getSessions(): Observable<Session[]> {
    return this.http.get<Session[]>(`${this.apiUrl}/sessions`);
  }

  // CREATE a session
  createSession(session: Session): Observable<Session> {
    return this.http.post<Session>(`${this.apiUrl}/sessions`, session);
  }

 // CREATE a Devision 
  getDivisions(): Observable<Session[]> {
    return this.http.get<Session[]>(`${this.apiUrl}/sessions`);
  }






  






  // ASSIGN participant (CORE LOGIC)
  assignParticipant(session: Session, participant: Participant): { success: boolean; message: string } {

    // Rule 1: Already assigned
    if (participant.assignedSession) {
      return { success: false, message: 'Participant already assigned to a session' };
    }

    // Rule 2: Session full
    if (session.participants.length >= session.capacity) {
      return { success: false, message: 'Session is already full' };
    }

    // Rule 3: Department limit exceeded
    const deptCount = session.participants.filter(
      p => p.department === participant.department
    ).length;

    const deptLimit = session.departmentLimits[participant.department];

    if (deptCount >= deptLimit) {
      return { success: false, message: `Department ${participant.department} limit reached` };
    }

    // VALID → Assign
    session.participants.push(participant);
    participant.assignedSession = session.id;

    return { success: true, message: 'Participant successfully assigned' };
  }

  // GET remaining seats
  getRemainingSeats(session: Session): number {
    return session.capacity - session.participants.length;
  }

  // GET remaining department seats
  getRemainingDeptSeats(session: Session, dept: 'A' | 'B' | 'C'): number {
    const used = session.participants.filter(p => p.department === dept).length;
    return session.departmentLimits[dept] - used;
  }
}