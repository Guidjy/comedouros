# comedouros
Backend do sistema de comedouros automáticos para ovinos

# observações

### **Autenticação**:
A autenticação de usuários no sistema é feita por meio de JSON Web Tokens - [Sobre](https://jwt.io/introduction), [npm](https://www.npmjs.com/package/jsonwebtoken)

# pacotes
1. django
2. djangorestframework
3. django-cors-headers
4. djangorestframework-simplejwt
5. Pillow

```pip install django djangorestframework django-cors-headers djangorestframework-simplejwt Pillow```

# apps
- comedouros (configurações)
- usuarios: registro, login e CRUD de usuários


# Rotas de api


## usuarios


### **'/usuarios/' - GET**:
lista todos os usuários do sistema

### **'/usuarios/{id}' - GET**:
lista dados do usuário {id}

### **'/usuarios/{id}' - PUT**:
Permite parcialmente editar os dados do usuário {id}
#### **corpo**:
```
obs: todos campos opcionais
{  
  "username":
  "email":  
  "first_name":  
  "last_name":  
  "is_staff":  
  "is_active":  
}
```

### **'/usuarios/{id}' - PATCH**:
Permite editar todos os dados do usuário {id}
#### **corpo**:
```
{  
  "username":
  "email":  
  "first_name":  
  "last_name":  
  "is_staff":  
  "is_active":  
}
```

### **'/usuarios/{id}' - DELETE**:
Deleta o usuário {id}


## login

### **'/api/token/' - POST**:
Realiza o login do usuário
#### **corpo**:
```
{
    "username":
    "password":
}
```
#### **resposta**:
```
{
    "refresh":
    "access":
}
```

### **'/api/token/refresh/' - POST**:
Retorna um novo token de acesso (usado quando o token atual expira)
#### **corpo**:
```
{
    "refresh": <refresh token>
}
```
#### **resposta**:
```
{
    "access": <access token>
}
```