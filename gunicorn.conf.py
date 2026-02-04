import multiprocessing
import os


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


workers = _int_env("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1)
threads = _int_env("GUNICORN_THREADS", 2)
timeout = _int_env("GUNICORN_TIMEOUT", 60)
graceful_timeout = _int_env("GUNICORN_GRACEFUL_TIMEOUT", 30)
keepalive = _int_env("GUNICORN_KEEPALIVE", 5)
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
