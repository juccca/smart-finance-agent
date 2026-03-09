# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Como o Tom utiliza? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Retomar o contexto de conversas anteriores com o usuário |
| `perfil_investidor.json` | JSON | Entender o perfil, objetivos e metas financeiras do usuário |
| `produtos_financeiros.json` | JSON | Explicar e comparar opções financeiras de acordo com o perfil |
| `transacoes.csv` | CSV | Identificar hábitos de gasto e oportunidades de melhoria |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados fictícios foram adaptados para refletir melhor o público-alvo do Tom: jovens adultos iniciantes em finanças.

Em `perfil_investidor.json`, o perfil foi atualizado: nome alterado para Lucas Mendes, idade reduzida para 24 anos, profissão trocada para Designer Freelancer e renda mensal ajustada para R$3.200. O perfil de investidor passou de moderado para conservador, e o patrimônio foi reduzido para valores mais condizentes com um jovem começando a poupar. A meta de "Entrada do apartamento" foi substituída por "Viagem internacional", mais realista para o perfil.

Em `produtos_financeiros.json`, o aporte mínimo do Tesouro Selic foi ajustado de R$30,00 para R$36,50, refletindo o valor real praticado. A Poupança foi adicionada como novo produto, por ser o primeiro contato de muitos iniciantes com o sistema financeiro.

Os arquivos `transacoes.csv` e `historico_atendimento.csv` não foram alterados.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades: injetar os dados diretamente no prompt (ctrl + c, ctrl + v) ou carregar os arquivos via código, como no exemplo abaixo.

```python
import pandas as pd
import json

# CSVs
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')

# JSONs
with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)

with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, fazendo com que o agente tenha o melhor contexto possível. Lembrando que, em soluções mais robustas, o ideal é que essas informações sejam carregadas dinamicamente para que possamos ganhar flexibilidade.

```text
DADOS DO CLIENTE E PERFIL (data/perfil_investidor.json):

{
  "nome": "Lucas Mendes",
  "idade": 24,
  "profissao": "Designer Freelancer",
  "renda_mensal": 3200.00,
  "perfil_investidor": "conservador",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 4800.00,
  "reserva_emergencia_atual": 1200.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 9600.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Viagem internacional",
      "valor_necessario": 8000.00,
      "prazo": "2027-01"
    }
  ]
}

TRANSAÇÕES DO CLIENTE (data/transacoes.csv):

data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

HISÓRICO DE ATENDIMENTO (data/historico_atendimento.csv):

data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

PRODUTOS DISPONÍVEIS PARA ENSINO (data/produtos_financeiros.json):

[
  {
    "nome": "Poupança",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "70% da Selic + TR",
    "aporte_minimo": 1.00,
    "indicado_para": "Primeiro contato com guardar dinheiro, apesar do rendimento limitado"
  },
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 36.50,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]

```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto montado abaixo se baseia na base original de conhecimento, mas os sintetiza, deixando apenas as informções mais relevantes e otimizando o consumo de tokens. Entretanto, vale lembrar que mais importante que economizar tokens, é ter todas as informações relevantes disponíveis em seu contexto.

```
DADOS DO CLIENTE:
- Nome: Lucas Mendes
- Perfil: Conservador
- Objetivo: Construir reserva de emergência
- Reserva atual: R$ 1.200 (meta: R$ 9.600)

RESUMO DE GASTOS:
- Moradia: R$ 1.200
- Alimentação: R$ 450
- Transporte: R$ 295
- Saúde: R$ 188
- Lazer: R$ 55,90
- Total de saídas: R$ 2.188,90

PRODUTOS DISPONÍVEIS PARA EXPLICAR:
- Poupança (risco baixo)
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Multimercado (risco médio)
- Fundo de Ações (risco alto)
```
