"""
Drop-in replacement for `timeout_decorator.timeout`.

CodeSignal runs on Linux and uses `timeout_decorator`, which relies on
`signal.SIGALRM`. That signal does not exist on Windows, so we fall back to a
thread-based timeout with the same decorator interface.
"""
import functools
import signal
import threading

try:
    if not hasattr(signal, "SIGALRM"):
        raise ImportError("SIGALRM not available on this platform")
    from timeout_decorator import timeout  # noqa: F401  (real CodeSignal decorator)
except ImportError:

    def timeout(seconds):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                outcome = {}

                def target():
                    try:
                        func(*args, **kwargs)
                    except BaseException as exc:  # propagate assertion errors etc.
                        outcome["error"] = exc

                worker = threading.Thread(target=target, daemon=True)
                worker.start()
                worker.join(seconds)
                if worker.is_alive():
                    raise TimeoutError(f"Timed Out ({seconds}s)")
                if "error" in outcome:
                    raise outcome["error"]

            return wrapper

        return decorator
