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

### (POST) '/accounts/api/token/'
Retorna dois JSON Web Tokens, um de access e outro de refresh (usados para autenticação).
corpo:
```
{
    "username": nome (string),
    "password": senha (string)
}
```

### (POST) '/accounts/api/token/refresh/'
Retorna um access token novo.
corpo:
```
{
    "refresh": nome (string)
}
```

### (GET, PUT, PATCH, DELETE) '/accounts/users/<user_id>(opcional)/'
Operações de Crud sobre os usuários.
| Método | Endpoint          | Ação                    |
| ------ | ----------------- | --------------          |
| GET    | `/users/`         | Lista todos             |
| GET    | `/users/{id}/`    | Busca um                |
| PUT    | `/users/{id}/`    | Atualização completa    |
| PATCH  | `/users/{id}/`    | Atualização parcial     |
| DELETE | `/users/{id}/`    | Deleta                  |
obs: Não usar método POST para criação de usuários. Usar rota '/accounts/register/' para isso.

### (GET) '/accounts/me/'
Retorna dados sobre o usuário logado atualmente.