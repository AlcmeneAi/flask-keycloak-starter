# Run Keycloak (fastest way)
One-liner (dev mode)

docker run --name keycloak -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev

# Flask + Keycloak (OIDC) Starter

Minimal Flask app with Keycloak login (OIDC) + logout.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set CLIENT_SECRET, etc.
./run.sh
```

Then open: http://localhost:5000
