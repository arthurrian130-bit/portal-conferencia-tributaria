import os
import importlib

def load_app_module():
    # Garante que variáveis de ambiente não quebrem o import
    os.environ.setdefault("PORTAL_TITLE", "Portal de Conferência Tributária")
    os.environ.setdefault("SIMPLES_URL", "https://simplesdash.manus.space")
    os.environ.setdefault("IRPJ_URL", "https://calc-fiscal-2etwmuhb.manus.space/")
    return importlib.import_module("app")

def test_home_ok():
    mod = load_app_module()
    client = mod.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200

def test_health_ok():
    mod = load_app_module()
    client = mod.app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200

def test_go_redirect():
    mod = load_app_module()
    client = mod.app.test_client()
    resp = client.get("/go/simples", follow_redirects=False)
    # redirect esperado (302 ou 301 dependendo do código)
    assert resp.status_code in (301, 302, 303, 307, 308)
