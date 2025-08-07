# comedouros
Comedouros automáticos

# Endpoints da api  

## Cadastro, login, e CRUD de usuários  

### (POST) '/accounts/register/':  
Cria um novo usuário.  
corpo:
```
{
    "username": nome (string),
    "email": email (string),
    "password": senha (string),
    "passwordConfirmation": senha novamente (string)
}
```
