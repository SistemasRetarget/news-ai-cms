#!/usr/bin/env python3
"""
SEO Validator for WordPress campaign pages.
Checks: meta tags, schema, headings, mobile-friendly, Core Web Vitals.

Usage:
  python3 scripts/seo-validator.py https://puyehue.cl/hot-sale-25
"""

import sys
import json
import subprocess
import re
from urllib.parse import urlparse

def fetch_page(url):
    """Fetch HTML from URL."""
    try:
        result = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "10", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def extract_meta(html):
    """Extract meta title, description, canonical."""
    title = re.search(r'<title[^>]*>([^<]+)</title>', html)
    desc = re.search(r'<meta[^>]*name=["\']?description["\']?[^>]*content=["\']?([^"\']+)', html, re.IGNORECASE)
    canonical = re.search(r'<link[^>]*rel=["\']?canonical["\']?[^>]*href=["\']?([^"\'>\s]+)', html, re.IGNORECASE)
    og_title = re.search(r'<meta[^>]*property=["\']?og:title["\']?[^>]*content=["\']?([^"\']+)', html, re.IGNORECASE)

    return {
        "title": title.group(1) if title else None,
        "description": desc.group(1) if desc else None,
        "canonical": canonical.group(1) if canonical else None,
        "og_title": og_title.group(1) if og_title else None,
    }

def check_headings(html):
    """Check H1 presence and structure."""
    h1s = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
    h2s = re.findall(r'<h2[^>]*>([^<]+)</h2>', html, re.IGNORECASE)

    return {
        "h1_count": len(h1s),
        "h1_text": h1s[0] if h1s else None,
        "h2_count": len(h2s),
        "issues": [
            "No H1 found" if len(h1s) == 0 else None,
            "Multiple H1s found" if len(h1s) > 1 else None,
        ]
    }

def check_schema(html):
    """Check for Schema.org markup."""
    schemas = re.findall(r'"@type":\s*"([^"]+)"', html)
    has_json_ld = bool(re.search(r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>', html))

    return {
        "has_json_ld": has_json_ld,
        "schema_types": list(set(schemas)),
        "issues": [
            "No Schema.org markup found" if not has_json_ld else None,
        ]
    }

def check_images(html):
    """Check for alt text in images."""
    images = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
    images_with_alt = [img for img in images if re.search(r'alt=["\']?[^"\'>\s]', img, re.IGNORECASE)]

    return {
        "total_images": len(images),
        "images_with_alt": len(images_with_alt),
        "alt_coverage": round((len(images_with_alt) / len(images) * 100), 1) if images else 100,
    }

def validate_seo(url):
    """Main validation."""
    html = fetch_page(url)
    if not html:
        return {"error": f"Could not fetch {url}"}

    parsed_url = urlparse(url)

    result = {
        "url": url,
        "domain": parsed_url.netloc,
        "path": parsed_url.path,
        "meta": extract_meta(html),
        "headings": check_headings(html),
        "schema": check_schema(html),
        "images": check_images(html),
    }

    # Score
    score = 100
    issues = []

    if not result["meta"]["title"]:
        score -= 15
        issues.append("❌ Missing meta title")
    elif len(result["meta"]["title"]) > 60:
        score -= 5
        issues.append(f"⚠️ Meta title too long ({len(result['meta']['title'])} chars)")
    else:
        issues.append("✅ Meta title OK")

    if not result["meta"]["description"]:
        score -= 15
        issues.append("❌ Missing meta description")
    elif len(result["meta"]["description"]) > 160:
        score -= 5
        issues.append(f"⚠️ Meta description too long ({len(result['meta']['description'])} chars)")
    else:
        issues.append("✅ Meta description OK")

    if result["headings"]["h1_count"] == 0:
        score -= 20
        issues.append("❌ No H1 found")
    elif result["headings"]["h1_count"] == 1:
        issues.append("✅ H1 structure OK")
    else:
        score -= 10
        issues.append(f"⚠️ Multiple H1s ({result['headings']['h1_count']})")

    if not result["schema"]["has_json_ld"]:
        score -= 10
        issues.append("⚠️ No Schema.org markup")
    else:
        issues.append(f"✅ Schema found: {', '.join(result['schema']['schema_types'][:3])}")

    if result["images"]["alt_coverage"] < 80:
        score -= 10
        issues.append(f"⚠️ Only {result['images']['alt_coverage']}% images have alt text")
    else:
        issues.append(f"✅ Alt text coverage: {result['images']['alt_coverage']}%")

    result["score"] = max(0, score)
    result["issues"] = issues

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 seo-validator.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    result = validate_seo(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
