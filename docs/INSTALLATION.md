# webFire: Installation and Setup Guide

This guide will walk you through the process of setting up and running the webFire application using Docker Compose.

## 1. Introduction

webFire is a web-based interface for managing the Uncomplicated Firewall (UFW). This document provides instructions to get the application up and running on your local machine.

## 2. Prerequisites

Before you begin, ensure you have the following software installed on your system:

*   **Git:** For cloning the project repository.
    *   [Download Git](https://git-scm.com/downloads)
*   **Docker:** For containerizing the application services.
    *   [Install Docker Engine](https://docs.docker.com/engine/install/)
*   **Docker Compose:** For defining and running multi-container Docker applications.
    *   Docker Compose is usually included with Docker Desktop installations. If not, refer to the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

## 3. Getting Started

Follow these steps to get webFire running:

1.  **Clone the Repository:**
    Open your terminal or command prompt and clone the webFire repository:
    ```bash
    git clone https://github.com/your-username/webFire.git # Replace with actual repository URL
    cd webFire
    ```

2.  **Build and Run the Containers:**
    Navigate to the root directory of the cloned repository (where `docker-compose.yml` is located) and run the following command:
    ```bash
    docker compose up --build
    ```
    This command will:
    *   Build the Docker images for both the backend (FastAPI) and frontend (Vue.js) services.
    *   Start the `backend`, `frontend` (build stage), and `nginx` services.
    *   The `nginx` service will serve the frontend and act as a reverse proxy for the backend API.

    The first time you run this, it might take a few minutes as Docker downloads base images and builds the application.

## 4. Accessing the Application

Once the containers are up and running, you can access webFire:

*   **Frontend (Web Interface):** Open your web browser and go to:
    [http://localhost](http://localhost)

*   **Backend API:** The backend API is accessible internally within the Docker network. If you need to access it directly for testing or development, it's exposed on:
    [http://localhost:8000/api](http://localhost:8000/api)

## 5. Initial Login (Development)

Authentication is enabled for development.

- Username: `admin`
- Password: `secret`

The backend issues JWTs at `/api/token` and protects all `/api/*` endpoints. Change the credentials and `SECRET_KEY` before any real deployment.

## 6. Stopping the Application

To stop the running Docker containers, press `Ctrl+C` in the terminal where `docker compose up` is running. Then, to remove the containers and networks, run:

```bash
docker compose down
```

To remove all volumes created by `docker compose up`, including the frontend build volume, add the `-v` flag:

```bash
docker compose down -v
```

## 7. UFW: container vs host firewall

The backend image includes `ufw` and required networking tools, and the container is granted `NET_ADMIN` and `NET_RAW` capabilities. This allows testing UFW commands inside the container.

Important: Managing `ufw` inside the container affects the container's network namespace, not the host firewall. For host-level firewall management, you would need to run the backend with host networking and additional privileges, and adjust Nginx accordingly. This is an advanced setup and should be done with caution.

If you want, create a compose override to run the backend with `network_mode: host` and proxy Nginx to `127.0.0.1:8000`.

### Use host networking (advanced)

An override file `docker-compose.hostnet.yml` is provided to run the backend on the host network and proxy Nginx to the host backend.

Start with the override:

```bash
docker compose -f docker-compose.yml -f docker-compose.hostnet.yml up --build
```

Notes:
- Backend binds directly to the host at `0.0.0.0:8000`.
- Nginx proxies to `http://host.docker.internal:8000` (Linux support added via `extra_hosts`).
- Managing `ufw` now affects the host firewall. Proceed with caution.
