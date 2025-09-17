# webFire

A modern, intuitive, and easy-to-use web-based user interface for managing the Uncomplicated Firewall (UFW).

## Features

*   Simplified UFW rule management (add, delete, modify)
*   Real-time firewall status and active rule display
*   User-friendly and responsive design
*   Accessible from any web browser

## Technology Stack

*   **Backend:** Python 3, FastAPI
*   **Frontend:** Vue.js, Vite, Tailwind CSS
*   **Containerization:** Docker, Docker Compose
*   **Web Server:** Nginx

## Getting Started

To get webFire up and running on your local machine, please refer to the detailed installation and setup guide:

➡️ [**INSTALLATION.md**](./docs/INSTALLATION.md)

## Project Structure

```
webFire/
├── backend/              # FastAPI backend application
├── frontend/             # Vue.js frontend application
├── docs/                 # Project documentation
│   └── INSTALLATION.md   # Installation and setup guide
├── nginx/                # Nginx configuration for reverse proxy
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```

## Development

For development purposes, you can run the services using Docker Compose as described in `INSTALLATION.md`. If you need to run the backend or frontend separately for debugging or specific development workflows:

### Backend Development

1.  Navigate to the `backend/` directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the FastAPI application:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://localhost:8000`.

### Frontend Development

1.  Navigate to the `frontend/` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the Vue.js development server:
    ```bash
    npm run dev
    ```
    The frontend will typically be available at `http://localhost:5173` (or another port as indicated by Vite).

## Testing

### Backend Tests

1.  Navigate to the `backend/` directory.
2.  Run pytest:
    ```bash
    pytest
    ```

### Frontend Tests

(Currently, no dedicated frontend tests are set up. This is a future enhancement.)

## Contributing

We welcome contributions to webFire! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon) for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (coming soon).
