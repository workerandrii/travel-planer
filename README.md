# Travel Planner API (Django + DRF)

A RESTful backend service built using **Django** and **Django REST Framework (DRF)** that helps travelers manage trips and collect locations from the Art Institute of Chicago Collections API.

## API Endpoint Blueprint Map

| HTTP Method | URL Path | Description |
| :--- | :--- | :--- |
| **GET** | `/api/projects/` | List all travel projects |
| **POST** | `/api/projects/` | Create project (with optional array of nested places) |
| **GET** | `/api/projects/{id}/` | Get a specific project details |
| **PUT/PATCH** | `/api/projects/{id}/` | Update project parameters |
| **DELETE** | `/api/projects/{id}/` | Remove project (Blocks if any contained places are visited) |
| **GET** | `/api/projects/{id}/places/` | List all places attached to a specific project |
| **POST** | `/api/projects/{id}/places/` | Append a new verified place to an existing project |
| **GET** | `/api/projects/{id}/places/{place_id}/` | Fetch data for a single place item |
| **PATCH** | `/api/projects/{id}/places/{place_id}/` | Update notes or mark place as `is_visited=true` |

## Getting Started

### Option 1: Run with Docker
1. Build and boot the local environment:
   ```bash
   docker build -t travel-planner-django .
   docker run -p 8000:8000 travel-planner-django