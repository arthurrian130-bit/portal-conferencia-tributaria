# Portal de Conferência Tributária — Versão 2 (Módulos + Histórico)

Este é um **portal/atalho em Python (Flask)** pensado para você abrir no **Cursor** e evoluir depois.
Ele permite:

- Cards de **módulos** (configuráveis)
- Ação **Abrir (registrar)** que passa por `/go/<id>` e grava no histórico
- Ação **Abrir aqui** que tenta embutir via iframe e registra como `embed`
- Página **Configurações** para editar/adicionar/remover módulos
- **Histórico em SQLite** (arquivo local)

> ⚠️ Alguns sites bloqueiam `iframe` por segurança. Nesse caso, use “Abrir em nova aba”.

## Rodar no Cursor (ou terminal)

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra:
- http://127.0.0.1:8000

## Configuração via .env

1) Copie `.env.example` para `.env`  
2) Edite os valores:

```env
PORTAL_TITLE="Portal de Conferência Tributária"
SIMPLES_URL="https://simplesdash.manus.space"
IRPJ_URL="https://calc-fiscal-2etwmuhb.manus.space/"
DB_PATH="./data/app.db"
SECRET_KEY="troque-esta-chave-em-producao"
```

## Onde fica o banco
- Por padrão: `./data/app.db`

## Endpoints úteis
- `/` Home
- `/go/<module_id>` registra no histórico e redireciona para o módulo
- `/track/<module_id>` registra “embed”
- `/settings` gerenciar módulos e histórico

## Ideias de evolução (perfeito para o Cursor)
- Login simples para proteger `/settings`
- Exportar histórico para CSV
- Tags por módulo (Simples, Presumido, Obrigações)
- “Favoritos” e busca
- Criar uma API `/api/modules` e `/api/history`

