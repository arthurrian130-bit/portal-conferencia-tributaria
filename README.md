# Portal de Conferência Tributária — Stateless

Portal Flask **stateless** para acesso rápido aos módulos tributários. Sem banco de dados, sem histórico e sem persistência.

## Rodar localmente

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### macOS / Linux (Bash)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse:
- http://127.0.0.1:8000

## Variáveis de ambiente

- `PORTAL_TITLE` (default: "Portal de Conferência Tributária")
- `SIMPLES_URL` (default: `https://simplesdash.manus.space`)
- `IRPJ_URL` (default: `https://calc-fiscal-2etwmuhb.manus.space/`)

Exemplo PowerShell:
```powershell
$env:PORTAL_TITLE="Portal de Conferência Tributária"
$env:SIMPLES_URL="https://simplesdash.manus.space"
$env:IRPJ_URL="https://calc-fiscal-2etwmuhb.manus.space/"
python app.py
```

Exemplo Bash:
```bash
export PORTAL_TITLE="Portal de Conferência Tributária"
export SIMPLES_URL="https://simplesdash.manus.space"
export IRPJ_URL="https://calc-fiscal-2etwmuhb.manus.space/"
python app.py
```

> Opcional: crie um arquivo `.env` com essas variáveis. O `app.py` carrega automaticamente.

## Produção (Render)

Build command:
```
pip install -r requirements.txt
```

Start command:
```
gunicorn app:app --config gunicorn.conf.py
```

### Deploy automatizado (Render Blueprint)

Este repositório inclui `render.yaml` para auto deploy. Basta conectar o repo no Render e habilitar.

### Deploy automático via GitHub Actions

1) No Render, copie o **Deploy Hook** do serviço.  
2) No GitHub, crie um secret chamado `RENDER_DEPLOY_HOOK_URL`.  
3) O workflow `.github/workflows/deploy.yml` dispara o deploy a cada push na `main`.

## Endpoints
- `/` Home
- `/go/<id>` redireciona para o módulo (`simples` e `irpj_csll`)
- `/about` Sobre
- `/help` Ajuda
- `/health` JSON de status

## Qualidade

- Lint: `ruff check .`
- Testes: `pytest -q`

## Automação de variáveis

Para padronizar as URLs dos módulos, use um arquivo `config.env` (ele é carregado automaticamente).

Exemplos:

```bash
cp config.env.example config.env
```

Ou gere automaticamente:

```powershell
.\scripts\set-env.ps1 -PortalTitle "Portal de Conferência Tributária" -SimplesUrl "https://..." -IrpjUrl "https://..."
```

```bash
./scripts/set-env.sh "Portal de Conferência Tributária" "https://..." "https://..."
```

## Ambiente de desenvolvimento

Para desativar cache de estáticos em dev, use:
```bash
APP_ENV=development
```
Em produção, mantenha o padrão `production`.

## Paleta de cores (UI)

As cores podem ser ajustadas no `static/styles.css` no bloco `:root`:

- `--bg`: `#0B1220`
- `--panel` / `--panel2`: `rgba(15, 25, 45, 0.65)`
- `--border` / `--border2`: `rgba(35, 48, 77, 0.6)`
- `--text`: `#E5E7EB`
- `--muted`: `#94A3B8`
- `--primary` (botão “Conferir”): `#3B82F6`
- `--primary-hover`: `#2563EB`
- `--success` (status online): `#22C55E`
- `--danger`: `#e24b4b`

## Troubleshooting (Render free)

Em planos gratuitos, o primeiro acesso pode demorar (cold start). Aguarde alguns segundos e tente novamente.
