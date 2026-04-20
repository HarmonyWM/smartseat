import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Data {
  API_URL = "http://localhost:5000/api";

  http = inject(HttpClient);

  post<T>(uri: string, data: any): Observable<T> {
    return this.http.post<T>(`${this.API_URL}/${uri}`, data);
  }

  get<T>(uri: string): Observable<T> {
    return this.http.get<T>(`${this.API_URL}/${uri}`);
  }

  put<T>(uri: string, data: any): Observable<T> {
    return this.http.put<T>(`${this.API_URL}/${uri}`, data);
  }

  delete<T>(uri: string): Observable<T> {
    return this.http.delete<T>(`${this.API_URL}/${uri}`);
  }
}
