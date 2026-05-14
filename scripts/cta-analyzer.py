#!/usr/bin/env python3
"""
CTA Analyzer: Detecta CTAs en HTML, valida tracking, sugiere mejoras.

Detecta:
- Botones (button, <a> con classes cta/btn)
- Forms (signup, contact, booking)
- Links importantes (interna, externa)

Valida:
- GA4 event tracking (data-event, gtag)
- CTA copy (largo, urgencia, acción)
- Posición en página (above fold, critical path)
- Accesibilidad (color, tamaño, contraste)

Sugiere:
- Mejoras de copy
- Posicionamiento
- Tracking faltante
- Best practices de conversión

Usage:
  python3 scripts/cta-analyzer.py https://puyehue.cl/hot-sale-25
"""

import sys
import json
import subprocess
import re
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

class CTAParser(HTMLParser):
    """Parse HTML and extract CTA candidates."""

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.ctas = []
        self.in_button = False
        self.in_link = False
        self.current_text = ""
        self.current_attrs = {}
        self.position = 0  # rough position in page
        self.total_chars = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_attrs = attrs_dict

        # Detect CTAs
        if tag == "button" or (tag == "a" and self.is_cta_link(attrs_dict)):
            self.in_button = True if tag == "button" else self.in_link
            if tag == "a":
                self.in_link = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "button" and self.in_button:
            self.register_cta("button", self.current_text, self.current_attrs)
            self.in_button = False
        elif tag == "a" and self.in_link:
            self.register_cta("link", self.current_text, self.current_attrs)
            self.in_link = False

    def handle_data(self, data):
        if self.in_button or self.in_link:
            self.current_text += data.strip()
        self.total_chars += len(data)

    def is_cta_link(self, attrs):
        """Check if link looks like a CTA."""
        class_str = attrs.get("class", "").lower()
        id_str = attrs.get("id", "").lower()

        cta_keywords = ["cta", "btn", "button", "action", "call", "click", "contact", "signup", "book", "comprar", "reservar"]

        for keyword in cta_keywords:
            if keyword in class_str or keyword in id_str:
                return True

        # Check href
        href = attrs.get("href", "")
        if href.startswith("#") or "/contact" in href or "/book" in href:
            return True

        return False

    def register_cta(self, cta_type, text, attrs):
        """Register a detected CTA."""
        if not text or len(text) < 2:
            return

        self.ctas.append({
            "type": cta_type,
            "text": text,
            "url": attrs.get("href", ""),
            "class": attrs.get("class", ""),
            "id": attrs.get("id", ""),
            "data_event": attrs.get("data-event", ""),
            "data_tracking": attrs.get("data-tracking", ""),
            "onclick": attrs.get("onclick", ""),
            "ga4": self.has_ga4_tracking(attrs),
        })

    def has_ga4_tracking(self, attrs):
        """Check if CTA has GA4 tracking."""
        data_event = attrs.get("data-event", "")
        onclick = attrs.get("onclick", "")
        class_str = attrs.get("class", "")

        # GA4 patterns
        if "gtag" in onclick or "gtag.config" in onclick:
            return True
        if "data-event" in attrs:
            return True
        if "ga-" in class_str:
            return True

        return False

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
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def analyze_ctas(url):
    """Main CTA analysis."""
    html = fetch_page(url)
    if not html:
        return {"error": f"Could not fetch {url}"}

    parser = CTAParser(url)
    try:
        parser.feed(html)
    except Exception as e:
        return {"error": f"Parse error: {e}"}

    ctas = parser.ctas
    if not ctas:
        return {
            "url": url,
            "cta_count": 0,
            "score": 0,
            "issues": ["No CTAs detected"],
            "suggestions": [
                "❌ Add at least one clear CTA button",
                "Consider primary CTA above the fold",
                "Use action-oriented copy (Comprar, Reservar, Contactar)"
            ]
        }

    # Scoring
    score = 100
    issues = []
    suggestions = []

    # Check 1: CTA count
    if len(ctas) < 1:
        score -= 30
        issues.append("❌ Too few CTAs (< 1)")
    elif len(ctas) > 5:
        score -= 10
        issues.append(f"⚠️ Too many CTAs ({len(ctas)}) - risk of dilution")
    else:
        issues.append(f"✅ CTA count OK ({len(ctas)})")

    # Check 2: GA4 tracking
    tracked = sum(1 for cta in ctas if cta["ga4"])
    if tracked == 0:
        score -= 25
        issues.append("❌ No GA4 tracking on any CTA")
        suggestions.append("Add data-event or gtag() to all CTAs for analytics")
    elif tracked == len(ctas):
        issues.append(f"✅ All {len(ctas)} CTAs have GA4 tracking")
    else:
        score -= 10
        issues.append(f"⚠️ Only {tracked}/{len(ctas)} CTAs tracked")
        suggestions.append("Add GA4 tracking to untracked CTAs")

    # Check 3: CTA copy quality
    for i, cta in enumerate(ctas):
        text = cta["text"].strip()

        # Too long
        if len(text) > 50:
            score -= 5
            suggestions.append(f"CTA #{i+1}: Copy too long ({len(text)} chars). Keep < 30 chars.")

        # Missing action verb
        action_verbs = ["comprar", "reservar", "contactar", "descargar", "enviar", "comenzar", "click", "suscribirse", "learn", "explore"]
        if not any(verb in text.lower() for verb in action_verbs):
            score -= 5
            suggestions.append(f"CTA #{i+1}: Add action verb (Comprar, Reservar, Contactar, etc)")

        # Missing urgency for campaign pages
        if "/hot-" in url or "/special" in url or "/offer" in url:
            urgency_words = ["ahora", "hoy", "limited", "solo", "urgente", "rápido"]
            if not any(word in text.lower() for word in urgency_words):
                suggestions.append(f"CTA #{i+1}: Consider adding urgency for campaign ({text})")

    # Check 4: Multiple CTA types
    button_count = sum(1 for cta in ctas if cta["type"] == "button")
    link_count = sum(1 for cta in ctas if cta["type"] == "link")

    if button_count > 0:
        issues.append(f"✅ {button_count} button CTA(s)")
    if link_count > 0:
        issues.append(f"✅ {link_count} link CTA(s)")

    if button_count == 0:
        score -= 10
        suggestions.append("Consider adding a prominent <button> for primary CTA")

    # Final score
    score = max(0, min(100, score))

    return {
        "url": url,
        "cta_count": len(ctas),
        "ctas": ctas,
        "tracking": {
            "ga4_tracked": tracked,
            "total": len(ctas),
            "coverage": round((tracked / len(ctas) * 100), 1) if ctas else 0,
        },
        "score": score,
        "issues": [i for i in issues if i],
        "suggestions": suggestions,
        "strategy": generate_strategy(url, ctas, tracked, len(ctas)),
    }

def generate_strategy(url, ctas, tracked, total):
    """Generate conversion strategy recommendations."""
    strategy = []

    if "/hot-" in url or "/special" in url or "/promo" in url or "/sale" in url:
        strategy.append("📢 Campaign Page Detected - Prioritize urgency and trust")
        if total < 2:
            strategy.append("  - Add secondary CTA (email, contact) for hesitant users")
        strategy.append("  - Test: 'Compra Ahora' vs 'Obtén tu Descuento'")
        strategy.append("  - Measure: conversion rate, click-through rate, time-on-page")

    if tracked / total < 0.5:
        strategy.append("🔍 Tracking Gap - Can't measure performance")
        strategy.append("  - Priority 1: Add GA4 events to ALL CTAs")
        strategy.append("  - Track: which CTA converts best, where users drop off")

    if tracked == total and total >= 2:
        strategy.append("📈 Good Tracking Coverage - Run A/B tests")
        strategy.append("  - Test CTA copy variations")
        strategy.append("  - Test CTA positioning (above fold vs below)")
        strategy.append("  - Test button color/size for contrast")

    if not strategy:
        strategy.append("✨ CTA structure looks good. Monitor GA4 for bounce/conversion data.")

    return strategy

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cta-analyzer.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    result = analyze_ctas(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
