# 🐄 API dos comedouros

- [Referências](https://docs.google.com/spreadsheets/d/15HQGgq4hI5UT0FyafI5cfC5hrJ-wvKuH/edit?gid=41191388#gid=41191388)
- [Requisitos](https://docs.google.com/document/d/1C0blKDuB74-u4f4hb53yxRGq7Ejbn0UwOHmLEz7ay6k/edit?tab=t.0)
- [Docs](https://drive.google.com/drive/folders/1Eoz59DTDh_xYlIQxQxaYbXVWdGcsk-re)
- [CSV](https://docs.google.com/spreadsheets/d/1f817qQpd2Z6koGriBVl8366EbcEyJZC12MkD0vI5sdY/edit?gid=1192282973#gid=1192282973)

Esta API fornece endpoints para gerenciar lotes, animais, brincos e refeições, bem como gerar relatórios de comportamento ingestivo, desempenho e viabilidade econômica.

Base URL:  
```
https://comedouros.onrender.com/
```

---

## 🧩 Índice

1. [Modelos e CRUD](#1-modelos-e-crud)
   - [Lotes](#lotes)
   - [Brincos](#brincos)
   - [Animais](#animais)
   - [Refeições](#refeições)
   - [Criação via CSV](#criação-via-csv)
2. [Comportamento Ingestivo](#2-comportamento-ingestivo)
   - [Consumo Diário](#consumo-diário)
   - [Minutos por Refeição](#minutos-por-refeição)
3. [Desempenho](#3-desempenho)
   - [Evolução do Peso](#evolução-do-peso)
   - [Evolução do Consumo Diário](#evolução-do-consumo-diário)
   - [Evolução do Ganho de Peso](#evolução-do-ganho-de-peso)
   - [Evolução do GMD](#evolução-do-gmd)
4. [Viabilidade Econômica](#4-viabilidade-econômica)
   - [Custo Total](#custo-total)
   - [Evolução do Custo Diário](#evolução-do-custo-diário)
   - [Ganho por Dia](#ganho-por-dia)
5. [Relatórios Gerais](#5-relatório-geral)

---

## 1. Modelos e CRUD

### **Lotes**

**Endpoint:**  
`/api/lotes/`

**Métodos:**
- `GET /lotes/` → Lista todos os lotes
- `GET /lotes/{id}/` → Retorna um lote específico
- `POST /lotes/` → Cria um novo lote
- `PUT /lotes/{id}/` → Atualiza um lote
- `DELETE /lotes/{id}/` → Remove um lote

**Exemplo de corpo (`POST`):**
```json
{
  "nome": "Lote 01",
  "n_animais": 10
}
```

**Exemplo de resposta (`GET /lotes/`):**
```json
[
  {
    "id": 1,
    "nome": "Lote 01",
    "n_animais": 10
  }
]
```

---

### **Brincos**

**Endpoint:**  
`/api/brincos/`

**Métodos:**
- `GET /brincos/`
- `GET /brincos/{id}/`
- `POST /brincos/`
- `PUT /brincos/{id}/`
- `DELETE /brincos/{id}/`

**Exemplo de corpo (`POST`):**
```json
{
  "tag_id": "TAG1234",
  "numero": "001"
}
```

---

### **Animais**

**Endpoint:**  
`/api/animais/`

**Métodos:**
- `GET /animais/`
- `GET /animais/{id}/`
- `POST /animais/`
- `PUT /animais/{id}/`
- `DELETE /animais/{id}/`

**Filtros disponíveis:**
- `?lote={id}`
- `?raca={string}`
- `?categoria={string}`

**Exemplo de corpo (`POST`):**
```json
{
  "sexo": "macho",
  "meses": 12,
  "raca": "Nelore",
  "categoria": "Bezerro",
  "frequencia_livre": false,
  "frequencia": 3,
  "brinco": 1,
  "lote": 2
}
```

**Resposta adicional:**
- `peso_atual`: peso vivo mais recente do animal (kg)

---

### **Refeições**

**Endpoint:**  
`/api/refeicoes/`

**Métodos:**
- `GET /refeicoes/`
- `GET /refeicoes/{id}/`
- `POST /refeicoes/`
- `PUT /refeicoes/{id}/`
- `DELETE /refeicoes/{id}/`

**Filtros disponíveis:**
- `?animal={id}`
- `?data=YYYY-MM-DD`

**Exemplo (`POST`):**
```json
{
  "horario_entrada": "09:00:00",
  "horario_saida": "09:20:00",
  "consumo_kg": 2.3,
  "peso_vivo_entrada_kg": 200.5,
  "data": "2025-10-10",
  "animal": 1
}
```

---

### **Criação via CSV**

**Endpoint:**  
`POST /api/cria-animais-com-csv/`

**Descrição:**  
Cria animais e suas refeições a partir de um arquivo CSV exportado do sistema do cocho.

**Requisição (multipart/form-data):**
| Campo | Tipo | Descrição |
|--------|------|------------|
| `arquivo` | file | Arquivo CSV contendo dados dos animais e refeições |

**Exemplo de resposta:**
```json
{
  "sucesso": "Animais e refeições registradas com sucesso"
}
```

---

## 2. Comportamento Ingestivo

### **Consumo Diário**

**Endpoints:**
```
GET /api/consumo-diario/animal/{brinco}/
GET /api/consumo-diario/animal/{brinco}/{data}/
GET /api/consumo-diario/lote/{nome}/
GET /api/consumo-diario/lote/{nome}/{data}/
```

**Descrição:**
- Retorna o consumo de ração (kg) de um **animal** ou **lote**, por dia ou por refeição em um dia específico.

**Parâmetros:**
| Nome | Tipo | Descrição |
|------|------|------------|
| `animal_ou_lote` | string | `'animal'` ou `'lote'` |
| `numero_ou_nome` | string | Número do brinco (animal) ou nome do lote |
| `data` | string (opcional) | `YYYY-MM-DD` |

**Resposta (animal):**
```json
{
  "2025-10-10": 3.2,
  "2025-10-11": 2.9
}
```

**Resposta (com data):**
```json
[
  {"09:00:00": 1.2},
  {"15:00:00": 1.7}
]
```

---

### **Minutos por Refeição**

**Endpoints:**
```
GET /api/minuto-por-refeicao/animal/{brinco}/
GET /api/minuto-por-refeicao/animal/{brinco}/{data}/
GET /api/minuto-por-refeicao/lote/{nome}/
```

**Descrição:**
Calcula o tempo médio (em minutos) das refeições de um animal ou lote.

**Resposta (animal, média por dia):**
```json
{
  "2025-10-10": 18.5,
  "2025-10-11": 21.3
}
```

**Resposta (animal, dia específico):**
```json
{
  "refeicao_n1": 17.5,
  "refeicao_n2": 19.0
}
```

---

## 3. Desempenho

Todos os endpoints de desempenho seguem o mesmo padrão de rota e aceitam tanto **animal** quanto **lote**:

```
GET /api/<rota>/<animal_ou_lote>/<numero_ou_nome>/
```

| Parâmetro | Tipo | Descrição |
|------------|------|------------|
| `animal_ou_lote` | string | `'animal'` ou `'lote'` |
| `numero_ou_nome` | string | Número do brinco (animal) ou nome do lote |

###  **Evolução do Peso**

**Endpoint:**  
`GET /api/evolucao-peso-por-dia/<animal_ou_lote>/<numero_ou_nome>/`

**Descrição:**  
Retorna a evolução do peso vivo (kg) de um animal ou lote ao longo do tempo.

**Exemplo (animal):**
```bash
GET /api/evolucao-peso-por-dia/animal/101/
```

**Exemplo (lote):**
```bash
GET /api/evolucao-peso-por-dia/lote/LoteA/
```

**Resposta:**
```json
{
  "2025-10-10": 200.5,
  "2025-10-11": 205.3
}
```

**Erros possíveis:**
```json
{"erro": "Não existe um animal com um brinco de número 101"}
```

---

###  **Evolução do Consumo Diário**

**Endpoint:**  
`GET /api/evolucao-consumo-diario/<animal_ou_lote>/<numero_ou_nome>/`

**Descrição:**  
Retorna o consumo diário de ração (kg) por animal ou lote.

**Exemplo (animal):**
```bash
GET /api/evolucao-consumo-diario/animal/101/
```

**Exemplo (lote):**
```bash
GET /api/evolucao-consumo-diario/lote/LoteA/
```

**Resposta:**
```json
{
  "2025-10-10": 3.0,
  "2025-10-11": 2.8
}
```

**Erros possíveis:**
```json
{"erro": "não foram encontradas refeições para o animal com o brinco 101"}
```

---

### **Evolução do Ganho de Peso**

**Endpoint:**  
`GET /api/evolucao-ganho/<animal_ou_lote>/<numero_ou_nome>/`

**Descrição:**  
Gera um relatório da evolução do ganho de peso de um animal ou lote.

**Exemplo (animal):**
```bash
GET /api/evolucao-ganho/animal/101/
```

**Exemplo (lote):**
```bash
GET /api/evolucao-ganho/lote/LoteA/
```

**Resposta:**
```json
{
  "2025-10-11": 4.8,
  "2025-10-12": 6.1
}
```

**Erros possíveis:**
```json
{"erro": "não foram encontrados animais para o lote LoteA"}
```

---

###  **Evolução do GMD (Ganho Médio Diário)**

**Endpoint:**  
`GET /api/evolucao-gmd/<animal_ou_lote>/<numero_ou_nome>/`

**Descrição:**  
Gera um relatório com o ganho médio diário (kg/dia) de um animal ou lote.

**Exemplo (animal):**
```bash
GET /api/evolucao-gmd/animal/101/
```

**Exemplo (lote):**
```bash
GET /api/evolucao-gmd/lote/LoteA/
```

**Resposta:**
```json
{
  "2025-10-10": 0.0,
  "2025-10-11": 2.3,
  "2025-10-12": 2.6
}
```

**Erros possíveis:**
```json
{"erro": "argumento invárlido 'gmd'"}
```

---

## 4. Viabilidade Econômica

### **Custo Total**

**Endpoints:**
```
GET /api/custo-total/animal/{brinco}/{preco_kg_racao}/
GET /api/custo-total/lote/{nome}/{preco_kg_racao}/
```

**Descrição:**
Calcula o custo total de ração consumida.

**Parâmetros:**
| Nome | Tipo | Descrição |
|------|------|------------|
| `preco_kg_racao` | float | Preço do kg da ração |

**Resposta:**
```json
{
  "custo_total": 324.5
}
```

---

### **Evolução do Custo Diário**

**Endpoints:**
```
GET /api/evolucao-custo-diario/animal/{brinco}/{preco_kg_racao}/
GET /api/evolucao-custo-diario/lote/{nome}/{preco_kg_racao}/
```

**Resposta:**
```json
{
  "2025-10-10": 15.6,
  "2025-10-11": 17.2
}
```

---

### **Ganho por Dia (em R$)**

**Endpoints:**
```
GET /api/ganho-por-dia/animal/{brinco}/{reais_por_kg_de_peso_vivo}/
GET /api/ganho-por-dia/lote/{nome}/{reais_por_kg_de_peso_vivo}/
```

**Descrição:**
Calcula o ganho em reais por dia, com base no GMD e no preço do kg do peso vivo.

**Parâmetros:**
| Nome | Tipo | Descrição |
|------|------|------------|
| `reais_por_kg_de_peso_vivo` | float | Preço (R$/kg) do peso vivo |

**Resposta:**
```json
{
  "2025-10-10": 9.8,
  "2025-10-11": 12.1
}
```

---

## 5. Relatório Geral

### **Relatório Geral Consolidado**

**Endpoint:**  
`GET /api/relatorio-geral/<animal_ou_lote>/<numero_ou_nome>/<preco_kg_racao>/<reais_por_kg_de_peso_vivo>/`

**Descrição:**  
Gera **um único relatório completo**, reunindo **todos os gráficos e métricas** já existentes na API, incluindo:
- Consumo diário
- Minutos por refeição
- Evolução do peso
- Evolução do consumo diário
- Evolução do ganho de peso
- Evolução do GMD
- Custo total
- Evolução do custo diário
- Ganho por dia

Funciona para **animal** e **lote**.

---

### 🔧 Parâmetros
| Parâmetro | Tipo | Descrição |
|-----------|------|------------|
| `animal_ou_lote` | string | `'animal'` ou `'lote'` |
| `numero_ou_nome` | string | Número do brinco (animal) ou nome do lote |
| `preco_kg_racao` | float (string) | Preço por kg da ração (formato `x.y`) |
| `reais_por_kg_de_peso_vivo` | float (string) | Preço do kg do peso vivo (formato `x.y`) |

---

### 📌 Exemplos de Requisição

#### Animal
```bash
GET /api/relatorio-geral/animal/101/2.5/14.3/
```

#### Lote
```bash
GET /api/relatorio-geral/lote/LoteA/2.5/14.3/
```

#### Todos os animais
```bash
GET /api/relatorio-geral/lote/TODOS/2.5/14.3/
```

---

### 📤 Exemplo de Resposta
```json
{
  "consumo_diario": {
    "2025-10-10": 3.1,
    "2025-10-11": 2.9
  },
  "minuto_por_refeicao": {
    "2025-10-10": 19.4,
    "2025-10-11": 20.1
  },
  "evolucao_peso_por_dia": {
    "2025-10-10": 200.5,
    "2025-10-11": 205.3
  },
  "evolucao_consumo_diario": {
    "2025-10-10": 3.0,
    "2025-10-11": 2.8
  },
  "evolucao_ganho": {
    "2025-10-11": 4.8,
    "2025-10-12": 6.1
  },
  "evolucao_gmd": {
    "2025-10-10": 0.0,
    "2025-10-11": 2.3
  },
  "custo_total": 324.5,
  "evolucao_custo_diario": {
    "2025-10-10": 15.6,
    "2025-10-11": 17.2
  },
  "ganho_por_dia": {
    "2025-10-10": 9.8,
    "2025-10-11": 12.1
  }
}
```

---


✅ **Observações gerais**
- Todas as respostas de erro seguem o formato:
```json
{"erro": "mensagem descritiva"}
```
- Datas devem estar no formato ISO: `YYYY-MM-DD`
- Valores monetários e numéricos devem usar ponto (`.`) como separador decimal.
