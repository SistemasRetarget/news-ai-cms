# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Build tools for native modules (sharp, pg)
RUN apk add --no-cache python3 make g++ libc6-compat

# Install all deps (devDeps needed for next build)
COPY package*.json ./
RUN npm ci

# Source code
COPY . .

# Placeholders so payload.config.ts compiles without a real DB.
# Real values are injected at runtime via Cloud Run secrets.
ARG DATABASE_URL=postgresql://build:build@localhost:5432/build
ARG PAYLOAD_SECRET=build-placeholder-secret
ENV DATABASE_URL=$DATABASE_URL
ENV PAYLOAD_SECRET=$PAYLOAD_SECRET
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_OPTIONS="--max_old_space_size=4096"

RUN npm run build

# ── Stage 2: runner ──────────────────────────────────────────────────────────
FROM node:20-alpine AS runner

WORKDIR /app

RUN apk add --no-cache libc6-compat

ENV NODE_ENV=production
ENV PORT=3000
ENV NEXT_TELEMETRY_DISABLED=1

# Copy built output and production deps only
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/payload.config.ts ./
COPY --from=builder /app/src ./src
COPY --from=builder /app/next.config.mjs ./

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD node -e "const p=process.env.PORT||3000;require('http').get('http://localhost:'+p,(r)=>{if(r.statusCode>=500)process.exit(1);}).on('error',()=>process.exit(1));"

CMD ["npm", "start"]
