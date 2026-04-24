import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Router } from "@angular/router";
import { CommonModule } from "@angular/common";
import { SentimentCountPipe } from "../sentiment-count.pipe";


interface Feedback {
  id: number;
  testo: string;
  sentiment: string;
  categoria: string;
  dataCreazione: Date;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, SentimentCountPipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  feedbacks: Feedback[] = [];
  isLoading: boolean = true;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.caricaFeedbacks();
  }

  caricaFeedbacks(): void {
    this.http.get<Feedback[]>('/api/feedbacks').subscribe({
      next: (data) => {
        this.feedbacks = data;
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }
  logout(): void {
    localStorage.removeItem('token_vip');
    this.router.navigate(['/login']);
  }
  getSentimentClass(sentiment: string): string {
    switch (sentiment) {
      case 'POSITIVE':
        return 'badge-positive';
      case 'NEGATIVE':
        return 'badge-negative';
        default: return 'badge-neutro';
    }
}
}