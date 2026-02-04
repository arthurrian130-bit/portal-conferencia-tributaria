from __future__ import annotations

import logging
import os
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, abort, jsonify, redirect, render_template, request

try:
    from flask_compress import Compress
except Exception:  # pragma: no cover - optional in some envs
    Compress = None  # type: ignore[assignment]


def load_dotenv(path: str = ".env") -> None:
    """Carrega um .env simples (KEY=VALUE) sem depender de bibliotecas externas."""
    p = Path(path)
    if not p.exists():
        return

    for raw_line in p.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip("'").strip('"')
        # Não sobrescreve env já definido
        os.environ.setdefault(k, v)


load_dotenv()
load_dotenv("config.env")

app = Flask(__name__)
app.config["PORTAL_TITLE"] = os.getenv("PORTAL_TITLE", "Portal de Conferência Tributária")
app.config["PORTAL_DESCRIPTION"] = os.getenv(
    "PORTAL_DESCRIPTION",
    "Portal stateless para acesso rápido aos módulos tributários.",
)
app.config["SIMPLES_URL"] = os.getenv("SIMPLES_URL", "https://simplesdash.manus.space")
app.config["IRPJ_URL"] = os.getenv("IRPJ_URL", "https://calc-fiscal-2etwmuhb.manus.space/")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000
app.config["APP_ENV"] = os.getenv("APP_ENV", "production")
app.config["COMPRESS_ALGORITHM"] = "gzip"
app.config["COMPRESS_MIN_SIZE"] = 512


def get_modules():
    return [
        {
            "id": "simples",
            "name": "Simples Nacional",
            "description": "Dashboard de cálculo/conferência do Simples Nacional.",
            "url": app.config["SIMPLES_URL"],
        },
        {
            "id": "irpj_csll",
            "name": "IRPJ + CSLL",
            "description": "Dashboard de cálculo/conferência de IRPJ e CSLL.",
            "url": app.config["IRPJ_URL"],
        },
    ]

def _get_preconnect_hints(modules):
    origins = set()
    dns_hosts = set()
    for m in modules:
        url = (m.get("url") or "").strip()
        if not url:
            continue
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            origin = f"{parsed.scheme}://{parsed.netloc}"
            origins.add(origin)
            dns_hosts.add(f"//{parsed.netloc}")
    return sorted(origins), sorted(dns_hosts)

def _configure_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


_configure_logging()

if Compress is not None:
    Compress(app)


@app.get("/")
def index():
    modules = get_modules()
    preconnect_origins, dns_prefetch_hosts = _get_preconnect_hints(modules)
    return render_template(
        "index.html",
        portal_title=app.config["PORTAL_TITLE"],
        portal_description=app.config["PORTAL_DESCRIPTION"],
        modules=modules,
        preconnect_origins=preconnect_origins,
        dns_prefetch_hosts=dns_prefetch_hosts,
    )


@app.get("/about")
def about():
    return render_template(
        "about.html",
        portal_title=app.config["PORTAL_TITLE"],
        portal_description=app.config["PORTAL_DESCRIPTION"],
        page_title="Sobre",
    )


@app.get("/help")
def help_page():
    return render_template(
        "help.html",
        portal_title=app.config["PORTAL_TITLE"],
        portal_description=app.config["PORTAL_DESCRIPTION"],
        page_title="Ajuda",
    )


@app.get("/go/<module_id>")
def go(module_id: str):
    modules = {m["id"]: m for m in get_modules()}
    module = modules.get(module_id)
    if not module:
        abort(404)
    return redirect(module["url"])

@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(404)
def not_found(_error):
    return (
        render_template(
            "404.html",
            portal_title=app.config["PORTAL_TITLE"],
            portal_description=app.config["PORTAL_DESCRIPTION"],
            page_title="Página não encontrada",
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(_error):
    return (
        render_template(
            "500.html",
        portal_title=app.config["PORTAL_TITLE"],
            portal_description=app.config["PORTAL_DESCRIPTION"],
            page_title="Erro interno",
        ),
        500,
    )


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self'; "
        "script-src 'self'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    if request.path.startswith("/static/"):
        if app.config["APP_ENV"].lower() == "development":
            response.headers.setdefault("Cache-Control", "no-store")
        else:
            response.headers.setdefault("Cache-Control", "public, max-age=31536000, immutable")
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
