#!/bin/bash
# Post-deploy SEO report: Lighthouse + SEO validator + Slack notification
# Usage: bash scripts/post-deploy-seo-report.sh https://puyehue.cl/hot-sale-25

set -e

URL="${1:-}"
if [ -z "$URL" ]; then
  echo "Usage: bash scripts/post-deploy-seo-report.sh <url>"
  exit 1
fi

TIMESTAMP=$(date +%s)
REPORT_DIR="/tmp/seo-reports"
mkdir -p "$REPORT_DIR"

echo "🔍 Running SEO report for: $URL"
echo ""

# 1. Run Lighthouse
echo "⏳ Lighthouse scan..."
LIGHTHOUSE_FILE="$REPORT_DIR/lighthouse-$TIMESTAMP.json"
lighthouse "$URL" --output=json --output-path="$LIGHTHOUSE_FILE" --chrome-flags="--headless --no-sandbox" 2>/dev/null || true

# Extract Lighthouse scores
if [ -f "$LIGHTHOUSE_FILE" ]; then
  LH_SCORE=$(jq '.categories.performance.score * 100 | round' "$LIGHTHOUSE_FILE" 2>/dev/null || echo "N/A")
  LH_ACCESSIBILITY=$(jq '.categories.accessibility.score * 100 | round' "$LIGHTHOUSE_FILE" 2>/dev/null || echo "N/A")
  LH_SEO=$(jq '.categories.seo.score * 100 | round' "$LIGHTHOUSE_FILE" 2>/dev/null || echo "N/A")
  LH_BEST_PRACTICES=$(jq '.categories["best-practices"].score * 100 | round' "$LIGHTHOUSE_FILE" 2>/dev/null || echo "N/A")
else
  LH_SCORE="Error"
  LH_ACCESSIBILITY="Error"
  LH_SEO="Error"
  LH_BEST_PRACTICES="Error"
fi

echo "✅ Lighthouse: Performance=$LH_SCORE Accessibility=$LH_ACCESSIBILITY SEO=$LH_SEO"
echo ""

# 2. Run custom SEO validator
echo "⏳ SEO validator..."
SEO_FILE="$REPORT_DIR/seo-$TIMESTAMP.json"
python3 scripts/seo-validator.py "$URL" > "$SEO_FILE" 2>/dev/null || true

if [ -f "$SEO_FILE" ]; then
  SEO_SCORE=$(jq '.score' "$SEO_FILE" 2>/dev/null || echo "N/A")
  SEO_ISSUES=$(jq -r '.issues[]' "$SEO_FILE" 2>/dev/null | head -5)
else
  SEO_SCORE="Error"
  SEO_ISSUES="Could not run validator"
fi

echo "✅ SEO Validator: Score=$SEO_SCORE"
echo ""

# 3. Run CTA analyzer
echo "⏳ CTA analyzer..."
CTA_FILE="$REPORT_DIR/cta-$TIMESTAMP.json"
python3 scripts/cta-analyzer.py "$URL" > "$CTA_FILE" 2>/dev/null || true

if [ -f "$CTA_FILE" ]; then
  CTA_SCORE=$(jq '.score' "$CTA_FILE" 2>/dev/null || echo "N/A")
  CTA_COUNT=$(jq '.cta_count' "$CTA_FILE" 2>/dev/null || echo "0")
  GA4_COVERAGE=$(jq '.tracking.coverage' "$CTA_FILE" 2>/dev/null || echo "0")
  CTA_ISSUES=$(jq -r '.suggestions[]' "$CTA_FILE" 2>/dev/null | head -3)
else
  CTA_SCORE="Error"
  CTA_COUNT="0"
  GA4_COVERAGE="0"
  CTA_ISSUES="Could not run analyzer"
fi

echo "✅ CTA Analyzer: Score=$CTA_SCORE CTAs=$CTA_COUNT GA4 Coverage=$GA4_COVERAGE%"
echo ""

# 4. Prepare Slack message (if SLACK_WEBHOOK_URL is set)
if [ -n "$SLACK_WEBHOOK_URL" ]; then
  echo "📤 Sending to Slack..."

  SLACK_MESSAGE=$(cat <<EOF
{
  "username": "COMPASS SEO Monitor",
  "icon_emoji": ":chart_with_upwards_trend:",
  "attachments": [
    {
      "color": "$([ "$SEO_SCORE" -ge 80 ] && echo 'good' || echo 'warning')",
      "title": "🚀 Post-Deploy SEO Report",
      "title_link": "$URL",
      "fields": [
        {
          "title": "📊 Lighthouse Scores",
          "value": "Performance: $LH_SCORE | Accessibility: $LH_ACCESSIBILITY | SEO: $LH_SEO | Best Practices: $LH_BEST_PRACTICES",
          "short": false
        },
        {
          "title": "✨ On-Page SEO Score",
          "value": "$SEO_SCORE/100",
          "short": true
        },
        {
          "title": "🎯 CTA Analysis",
          "value": "Score: $CTA_SCORE/100 | CTAs: $CTA_COUNT | GA4 Coverage: $GA4_COVERAGE%",
          "short": true
        },
        {
          "title": "🔍 SEO Issues",
          "value": "\`\`\`$SEO_ISSUES\`\`\`",
          "short": false
        },
        {
          "title": "💡 CTA Suggestions",
          "value": "\`\`\`$CTA_ISSUES\`\`\`",
          "short": false
        },
        {
          "title": "🔗 URL",
          "value": "<$URL|$URL>",
          "short": false
        }
      ],
      "footer": "COMPASS SEO Monitor",
      "ts": $(date +%s)
    }
  ]
}
EOF
  )

  curl -X POST -H 'Content-type: application/json' \
    --data "$SLACK_MESSAGE" \
    "$SLACK_WEBHOOK_URL" 2>/dev/null || true

  echo "✅ Slack notification sent"
else
  echo "⚠️  SLACK_WEBHOOK_URL not set - skipping Slack notification"
fi

echo ""
echo "📈 Full reports saved to:"
echo "  - Lighthouse: $LIGHTHOUSE_FILE"
echo "  - SEO Validator: $SEO_FILE"
echo "  - CTA Analyzer: $CTA_FILE"
echo ""
echo "Done! 🎉"
