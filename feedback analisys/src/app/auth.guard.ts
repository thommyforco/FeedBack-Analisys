import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";

export const authGuard: CanActivateFn = (route, state) => {
    const token = localStorage.getItem('token_vip');        
    if (token) {
        // Se c'è un token, allora l'utente è autenticato: può accedere alla rotta protetta
        return true;
    }
    // Se non c'è un token, allora l'utente NON è autenticato: lo reindirizziamo alla pagina di login
    const router = inject(Router);
    return router.createUrlTree(['/login']);
};