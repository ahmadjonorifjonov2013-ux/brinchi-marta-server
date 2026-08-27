import hashlib
from urllib.parse import urlencode


def build_cache_key(prefix, request, user_scoped=False):
    params = sorted(request.query_params.items())
    raw = urlencode(params)

    if user_scoped:
        uid = request.user.id if request.user.is_authenticated else "anon"
        raw = f"u{uid}|{raw}"

    digest = hashlib.md5(raw.encode()).hexdigest()[:12]
    return f"{prefix}:{digest}"