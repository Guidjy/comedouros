# comedouros
Comedouros automáticos
- [Referências](https://docs.google.com/spreadsheets/d/15HQGgq4hI5UT0FyafI5cfC5hrJ-wvKuH/edit?gid=41191388#gid=41191388)
- [Requisitos](https://docs.google.com/document/d/1C0blKDuB74-u4f4hb53yxRGq7Ejbn0UwOHmLEz7ay6k/edit?tab=t.0)
- [Docs](https://drive.google.com/drive/folders/1Eoz59DTDh_xYlIQxQxaYbXVWdGcsk-re)

# Endpoints da api  

## 1. Cadastro, login, e CRUD de usuários  

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


## 2. Operações CRUD

### Lotes

**Endpoint:** `/lotes/`
**Método:** GET, POST, PUT, PATCH, DELETE
**Descrição:** Operações CRUD para o modelo `Lote`.

### Brincos

**Endpoint:** `/brincos/`
**Método:** GET, POST, PUT, PATCH, DELETE
**Descrição:** Operações CRUD para o modelo `Brinco`.

### Animais

**Endpoint:** `/animais/`
**Método:** GET, POST, PUT, PATCH, DELETE
**Descrição:** Operações CRUD para o modelo `Animal`.
**Filtros disponíveis:** `lote`, `raca`, `categoria`
**Observações:**

* O campo `peso_atual` é adicionado automaticamente na resposta de `retrieve` e `list`.

### Refeições

**Endpoint:** `/refeicoes/`
**Método:** GET, POST, PUT, PATCH, DELETE
**Descrição:** Operações CRUD para o modelo `Refeicao`.
**Filtros disponíveis:** `animal`, `data`
**Ordenação padrão:** `data` decrescente

### Upload de CSV de animais

**Endpoint:** `/cria-animais-com-csv/`
**Método:** POST
**Descrição:** Cria animais e refeições a partir de um arquivo CSV.
**Parâmetros:**

* `arquivo` (arquivo CSV)

**Retorno:**

```json
{ "sucesso": "Animais e refeições registradas com sucesso" }
```

## 2. Comportamento Ingestivo

### Consumo diário

**Endpoint:** `/consumo-diario/<animal_ou_lote>/<numero>/` ou `/consumo-diario/<animal_ou_lote>/<numero>/<data>/`
**Método:** GET
**Descrição:** Retorna o consumo diário de um animal ou lote.
**Parâmetros:**

* `animal_ou_lote`: `animal` ou `lote`
* `numero`: número do brinco ou id do lote
* `data` (opcional): filtra por data específica

### Minuto por refeição

**Endpoint:** `/minuto-por-refeicao/<animal_ou_lote>/<numero>/` ou `/minuto-por-refeicao/<animal_ou_lote>/<numero>/<data>/`
**Método:** GET
**Descrição:** Retorna o tempo médio gasto por refeição.
**Parâmetros:**

* `animal_ou_lote`: `animal` ou `lote`
* `numero`: número do brinco ou id do lote
* `data` (opcional): filtra por data específica

## 3. Desempenho

### Evolução do peso por dia

**Endpoint:** `/evolucao-peso-por-dia/<numero>/`
**Método:** GET
**Descrição:** Retorna a evolução do peso vivo de um animal.
**Parâmetros:**

* `numero`: número do brinco do animal

### Evolução do consumo diário

**Endpoint:** `/evolucao-consumo-diario/<animal_ou_lote>/<numero>/`
**Método:** GET
**Descrição:** Retorna a evolução do consumo diário de um animal ou lote.
**Parâmetros:**

* `animal_ou_lote`: `animal` ou `lote`
* `numero`: número do brinco ou id do lote

### Evolução do ganho de peso

**Endpoint:** `/evolucao-ganho/<numero>/`
**Método:** GET
**Descrição:** Retorna a evolução do ganho de peso de um animal.
**Parâmetros:**

* `numero`: número do brinco do animal

### Evolução do GMD (Ganho Médio Diário)

**Endpoint:** `/evolucao-gmd/<numero>/`
**Método:** GET
**Descrição:** Retorna a evolução do ganho médio diário de um animal.
**Parâmetros:**

* `numero`: número do brinco do animal


