#!/usr/bin/env python3
"""
Detecta páginas de campaña activas en los sitios WordPress de Retarget.

Consulta WP REST API de cada sitio, filtra páginas publicadas con slugs
de campaña, retorna lista de URLs para validar.

Usage:
  python3 scripts/wp-campaign-discovery.py
  python3 scripts/wp-campaign-discovery.py --json   # output JSON puro
"""

import sys
import json
import subprocess
import re
import os
import argparse

CAMPAIGN_KEYWORDS = [
    "hot-sale", "hotsale", "hot_sale",
    "promo", "promocion",
    "cyber", "cyberlunes",
    "travel-sale", "travelsale",
    "oferta", "descuento", "dcto",
    "sale", "especial",
    "daypass", "day-pass", "ven-por-el-dia",
    "piscina", "4x3", "5x4",
    "nueva-promocion",
]

SITES = [
    {
        "name": "Puyehue",
        "base": "https://puyehue.cl",
        "cookies": None,
        "auth_env": ("WP_PUYEHUE_USER", "WP_PUYEHUE_PASS"),
    },
    {
        "name": "TAC (Termas Aguas Calientes)",
        "base": "https://termasaguascalientes.cl",
        "cookies": "/tmp/tac_cookies2.txt",
        "auth_env": None,
    },
    {
        "name": "Futangue",
        "base": "https://parquefutangue.com",
        "cookies": "/tmp/futangue_cookies2.txt",
        "auth_env": None,
    },
]


def is_campaign_slug(slug):
    slug_lower = slug.lower()
    return any(kw in slug_lower for kw in CAMPAIGN_KEYWORDS)


def fetch_pages(site):
    base = site["base"]
    url = f"{base}/wp-json/wp/v2/pages?per_page=100&status=publish&_fields=id,slug,link,status"

    cmd = ["curl", "-sS", "-L", "--max-time", "15"]

    # Auth: cookies file
    cookies = site.get("cookies")
    if cookies and os.path.exists(cookies):
        cmd += ["--cookie", cookies]

    # Auth: basic auth from env
    auth_env = site.get("auth_env")
    if auth_env:
        user = os.environ.get(auth_env[0], "")
        passwd = os.environ.get(auth_env[1], "")
        if user and passwd:
            cmd += ["-u", f"{user}:{passwd}"]

    cmd.append(url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode == 0 and result.stdout.strip().startswith("["):
            return json.loads(result.stdout)
        return []
    except Exception:
        return []


def discover_campaigns():
    found = []

    for site in SITES:
        pages = fetch_pages(site)
        campaign_pages = [p for p in pages if is_campaign_slug(p.get("slug", ""))]

        for page in campaign_pages:
            found.append({
                "site": site["name"],
                "slug": page["slug"],
                "url": page["link"].rstrip("/"),
            })

    return found


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output as JSON array")
    args = parser.parse_args()

    campaigns = discover_campaigns()

    if args.json:
        print(json.dumps(campaigns, indent=2, ensure_ascii=False))
    else:
        if not campaigns:
            print("No campaign pages detected.")
            sys.exit(0)

        print(f"🎯 {len(campaigns)} campaign page(s) detected:\n")
        for c in campaigns:
            print(f"  [{c['site']}] {c['slug']}")
            print(f"    {c['url']}")
        print()
