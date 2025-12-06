# Environment Variables Setup Guide

This project now uses environment variables for port configuration. Follow these steps to set up your environment.

## Backend Setup

1. Create a `.env` file in the root directory (same level as `main.py`) with the following content:

```env
# Backend Configuration
BACKEND_PORT=8001
BACKEND_HOST=127.0.0.1
```

2. To run the backend, use the new run script:

```bash
python run_backend.py
```

This will automatically read the port from the `.env` file. The default port is 8001 if not specified.

## Frontend Setup

1. Create a `.env` file in `frontend/school-management-system/` directory with the following content:

```env
# Frontend Configuration
VITE_API_BASE_URL=http://127.0.0.1:8001

# Frontend Port (used by Vite dev server)
VITE_PORT=5173
```

2. The frontend will automatically use `VITE_API_BASE_URL` for all API calls. Make sure this matches your backend port.

3. To change the backend port, simply update `VITE_API_BASE_URL` in the frontend `.env` file and `BACKEND_PORT` in the backend `.env` file to match.

## Important Notes

- **Vite Environment Variables**: In Vite, environment variables must be prefixed with `VITE_` to be accessible in the frontend code.
- **Backend Port**: The backend uses `python-dotenv` to load environment variables from `.env` file.
- **No Code Changes Needed**: Once the `.env` files are set up, you can change ports by simply editing the `.env` files - no code changes required!

## Example: Changing Ports

If you want to change the backend port to 3000:

**Backend `.env`:**
```env
BACKEND_PORT=3000
BACKEND_HOST=127.0.0.1
```

**Frontend `.env`:**
```env
VITE_API_BASE_URL=http://127.0.0.1:3000
VITE_PORT=5173
```

That's it! The application will automatically use the new ports.


