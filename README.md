# comedouros
Comedouros automáticos
- [Referências](https://docs.google.com/spreadsheets/d/15HQGgq4hI5UT0FyafI5cfC5hrJ-wvKuH/edit?gid=41191388#gid=41191388)
- [Requisitos](https://docs.google.com/document/d/1C0blKDuB74-u4f4hb53yxRGq7Ejbn0UwOHmLEz7ay6k/edit?tab=t.0)

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
    "refresh": refresh token
}
```

### (GET, PUT, PATCH, DELETE) '/accounts/users/<user_id>(opcional)/'
Operações de Crud sobre os usuários.  
obs: Não usar método POST para criação de usuários. Usar rota '/accounts/register/' para isso.

### (GET) '/accounts/me/'
Retorna dados sobre o usuário logado atualmente.


## CRUD de animais e refeições


Esses endpoints permitem criar, listar, atualizar e excluir registros relacionados a **lotes**, **raças**, **brincos**, **animais** e **refeições**.

ADICIONAR AQUI

---

