"""Configuration loaded from a local .env file."""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
import truststore

# Use Windows' trusted certificate store instead of weakening HTTPS validation.
truststore.inject_into_ssl()
load_dotenv(Path(__file__).with_name('.env'))


def supabase_settings() -> tuple[str, str]:
    url = os.getenv('SUPABASE_URL', '').strip()
    # SUPABASE_KEY is accepted only for compatibility with an older local file.
    key = os.getenv('SUPABASE_SECRET_KEY', os.getenv('SUPABASE_KEY', '')).strip()
    if not url or not key:
        raise RuntimeError('Configure SUPABASE_URL e SUPABASE_SECRET_KEY no arquivo .env.')
    return url, key

