## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and consistent environments.

### Requirements
- **Docker** and **Docker Compose** installed on your system.
- The project uses **Python 3.13-slim** as the base image (see `Dockerfile`).
- Dependencies are managed via `requirements.txt` and installed in a virtual environment inside the container.

### Environment Variables
- The application can be configured using environment variables. Example values are provided in `.env.example`.
- To use custom environment variables, copy `.env.example` to `.env` and adjust as needed.
- Uncomment the `env_file: ./.env` line in `docker-compose.yml` to enable loading environment variables from your `.env` file.

### Services
- **python-app**: The main application container. No ports are exposed by default. If your `main.py` provides an API or web server, expose the necessary ports by uncommenting and editing the `ports:` section in `docker-compose.yml`.
- **minio**: Object storage service. Exposes:
  - `9000:9000` (MinIO API)
  - `9001:9001` (MinIO Console)
  - Default credentials: `minioadmin` / `minioadmin`
  - Data is persisted in the `minio-data` Docker volume.

### Build and Run Instructions
1. (Optional) Copy `.env.example` to `.env` and edit as needed for your environment.
2. Build and start the services:
   ```sh
   docker compose up --build
   ```
3. To stop the services:
   ```sh
   docker compose down
   ```

### Special Configuration
- The application runs as a non-root user (`appuser`) inside the container for improved security.
- All dependencies are installed in a Python virtual environment within the container.
- The `python-app` service depends on MinIO and will wait for it to be available.
- If you need to expose application ports (e.g., for a web API), edit the `ports:` section under `python-app` in `docker-compose.yml`.

---

_This section was updated to reflect the current Docker-based setup for the project._
