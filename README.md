# webFire

Modern, web-based management for UFW (Uncomplicated Firewall) with a FastAPI backend and a Vue 3 UI, packaged behind Nginx.

## Highlights

- UFW status and rules at a glance
- Add, delete, and filter rules with stable rule IDs
- JWT-protected API with a simple dev login
- Dockerized stack with Nginx reverse proxy

## Architecture

- Backend: FastAPI (`backend/`) exposes `/api/*` endpoints and Swagger at `/docs`
- Frontend: Vue 3 + Vite (`frontend/`) builds to static assets served by Nginx
- Web server: Nginx (`nginx/`) serves the SPA and proxies `/api` to the backend
- Compose: `docker-compose.yml` builds all services and stitches them together

Default ports (compose):
- `http://localhost:4280` → Nginx (frontend + API proxy)
- `http://localhost:4200` → Backend (debug access; not needed in normal use)

See the full installation walkthrough in docs/INSTALLATION.md.

## Quick Start

Run the full stack via Docker Compose:

```bash
docker compose up --build
```

Then open `http://localhost:4280`.

Authentication (development):
- Username: `admin`
- Password: `secret`

Change `SECRET_KEY` and credentials before any real deployment.

## API Overview

Base path: `/api`

- Auth: `POST /api/token` (form fields `username`, `password`)
- Status: `GET /api/status`
- Rules: `GET /api/rules`
- Add Rule: `POST /api/rules` (JSON body)
- Delete Rule: `DELETE /api/rules/{id}`
- Enable UFW: `POST /api/enable`
- Disable UFW: `POST /api/disable`

OpenAPI docs: `/docs` and `/redoc` (proxied by Nginx)

Example: fetch a token with curl

```bash
curl -s -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=secret' \
  http://localhost:4280/api/token
```

## Development

You can use Docker (recommended) or run services locally.

### Backend (local)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Environment variables:
- `SECRET_KEY` (required for JWT; defaults to an insecure value in dev)

### Frontend (local)

```bash
cd frontend
npm install
npm run dev
```

By default the frontend calls `/api` (behind Nginx). To point the UI at a locally running backend, set:

```bash
VITE_API_BASE_URL=http://localhost:8000/api npm run dev
```

## Security and Privileges

- The backend executes `ufw` via `sudo` and the compose grants `NET_ADMIN`/`NET_RAW` to the container.
- Out of the box, UFW commands affect the container namespace. To manage the host firewall, use the provided host networking override and proceed with caution.
- Change `SECRET_KEY` and harden authentication before exposing to untrusted networks.

Related docs: docs/INSTALLATION.md and scripts/configure_ufw_for_docker.sh.

## Project Structure

```
webFire/
├── backend/                  FastAPI app and UFW service
│   ├── main.py               API endpoints, auth, CORS
│   ├── ufw_service.py        UFW status/rules and operations
│   ├── auth.py               JWT + password hashing helpers
│   ├── tests/                API and service tests
│   └── Dockerfile            Backend image (installs ufw)
├── frontend/                 Vue 3 app
│   ├── src/                  Views, components, stores, axios client
│   └── Dockerfile            Frontend build image
├── nginx/                    Reverse proxy configs
├── scripts/                  Utility scripts (e.g., UFW + Docker)
├── docker-compose.yml        Default stack (Nginx + API + UI)
├── docker-compose.hostnet.yml Host-network override (advanced)
└── docs/INSTALLATION.md      Detailed setup guide
```

## Testing

Backend tests use pytest and FastAPI’s TestClient:

```bash
cd backend
pytest
```

Frontend currently has no automated tests. Contributions welcome.

## Contributing

Issues and PRs are welcome. Please propose changes with clear rationale and, when possible, tests.

## License

Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
See `LICENSE.md` for full text. By contributing, you agree to license
your contributions under the AGPL-3.0.
