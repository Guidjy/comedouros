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

```pip install django djangorestframework django-cors-headers djangorestframework-simplejwt```

# apps
- comedouros (configurações)
- usuarios: registro, login e CRUD de usuários

# Rotas de api

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