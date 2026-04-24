import { Component } from '@angular/core';
import {Router} from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  password = '';
  username = '';

  constructor(private http: HttpClient, private router: Router) {}

  public onLoginClick(username : String, password : String) {
    const credenziali = {username: username, password: password};
    this.http.post('/api/login', credenziali).subscribe({
      
      next: (rispostaDelBackend: any) => {
        // SUCCESSO: Il login è andato a buon fine!
        
        // A. Salviamo il "Pass VIP" (Token) nella memoria del browser
        localStorage.setItem('token_vip', rispostaDelBackend.token);
        
        // B. IL REINDIRIZZAMENTO: Diciamo al Router di portarci alla dashboard
        this.router.navigate(['/dashboard']); 
      },
      
      error: (errore) => {
        // FALLIMENTO: Password sbagliata o utente non trovato
        alert('Attenzione: Email o Password errati!');
      }
    });
  }
}
