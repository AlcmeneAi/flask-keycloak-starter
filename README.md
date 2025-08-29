# Flask + Keycloak (OIDC) Starter

A minimal Flask application demonstrating authentication and logout using Keycloak via OpenID Connect (OIDC).  
This repo is ideal for quickly prototyping or learning how to integrate Keycloak with Flask.

## Features

- Keycloak login and logout (OIDC)
- Minimal Flask setup
- Quick local development

## Prerequisites

- [Docker](https://www.docker.com/) (for running Keycloak)
- Python 3.8+ recommended

## Running Keycloak (Dev Mode)

Start a local Keycloak server using Docker:

```bash
docker run --name keycloak -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev
```

Access Keycloak admin console at [http://localhost:8080](http://localhost:8080)  
Login with `admin` / `admin`.

## Setup Flask App

Clone this repo and set up the Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in your Keycloak configuration:

```
KEYCLOAK_CLIENT_ID=
KEYCLOAK_CLIENT_SECRET=
KEYCLOAK_REALM=
KEYCLOAK_URL=
```

> **Note**: You must set these values to match the client configuration in your Keycloak instance.

Run the Flask app:

```bash
./run.sh
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- Login via Keycloak
- View protected pages
- Logout

## Customization

Adjust the Flask routes or Keycloak configuration in `.env` to fit your needs.

## Contributing

Pull requests and issues are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) if available.

## License

MIT License. See [LICENSE](LICENSE).

## Resources

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Flask Documentation](https://flask.palletsprojects.com/)
