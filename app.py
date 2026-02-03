from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, abort, redirect, render_template


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

app = Flask(__name__)
app.config["PORTAL_TITLE"] = os.getenv("PORTAL_TITLE", "Portal de Conferência Tributária")
app.config["SIMPLES_URL"] = os.getenv("SIMPLES_URL", "https://simplesdash.manus.space")
app.config["IRPJ_URL"] = os.getenv("IRPJ_URL", "https://calc-fiscal-2etwmuhb.manus.space/")
@app.get("/health")
def health():
    return {"status": "ok"}


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


@app.get("/")
def index():
    modules = get_modules()
    preconnect_origins, dns_prefetch_hosts = _get_preconnect_hints(modules)
    return render_template(
        "index.html",
        portal_title=app.config["PORTAL_TITLE"],
        modules=modules,
        preconnect_origins=preconnect_origins,
        dns_prefetch_hosts=dns_prefetch_hosts,
    )


@app.get("/go/<module_id>")
def go(module_id: str):
    modules = {m["id"]: m for m in get_modules()}
    module = modules.get(module_id)
    if not module:
        abort(404)
    return redirect(module["url"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
