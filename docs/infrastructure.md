# Infrastructure Overview

This document outlines the core infrastructure of the eval-track project, including its services, databases, storage solutions, and deployment configurations.

## Architecture Overview

The eval-track project consists of several interconnected services:

- **tracker-py**: Python-based tracing service for collecting and managing trace data
- **web**: Next.js frontend application with Auth0 authentication
- **postgres**: Primary database for storing application data
- **minio**: S3-compatible object storage for artifacts
- **redis**: Caching and queue management
- **inngest**: Event processing and background job management
- **redisinsight**: Redis monitoring and management interface

## Services

### tracker-py (Tracing Service)

The tracker-py service is the core Python-based tracing service responsible for collecting and managing trace data.

**Container Details:**
- **Port:** 8080
- **Build Context:** ./tracker-py
- **Development Mode:** Hot reload enabled for local development
- **Dependencies:** PostgreSQL database for trace storage

**Key Environment Variables:**
- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_USER`: Database user for authentication
- `POSTGRES_DATABASE`: Target database name

**Service Interactions:**
- Provides tracing API endpoints consumed by the web frontend
- Stores trace data in PostgreSQL database
- Integrates with MinIO for artifact storage when needed

**Local vs Production:**
- Local: Uses Docker build with hot reload
- Production: TBD (deployment details to be documented)

### web (Next.js Frontend)

The web service provides the frontend interface for the eval-track project, built with Next.js and integrated with Auth0 for authentication.

**Container Details:**
- **Port:** 3000
- **Build Context:** ./web
- **Development Mode:** Uses pnpm dev for hot reload
- **Dependencies:** PostgreSQL, Inngest, Redis

**Key Environment Variables:**
- `DATABASE_URL`: PostgreSQL connection string for Prisma
- `BETTER_AUTH_SECRET`: Authentication secret for better-auth
- `BETTER_AUTH_URL`: Authentication callback URL
- `INNGEST_DEV`: Inngest development mode flag
- `INNGEST_BASE_URL`: Inngest service URL
- `INNGEST_EVENT_KEY`: Event key for Inngest
- `INNGEST_SIGNING_KEY`: Signing key for Inngest

**Service Interactions:**
- Connects to tracker-py for trace data management
- Uses PostgreSQL through Prisma ORM
- Integrates with Inngest for background job processing
- Uses Redis (through Inngest) for job queue management
- Implements Auth0 for user authentication

**Local vs Production:**
- Local: Uses pnpm dev with hot reload and volume mounting
- Production: TBD (deployment details to be documented)

### minio (Object Storage)

MinIO provides S3-compatible object storage for storing artifacts and other binary data.

**Container Details:**
- **Ports:** 
  - 4569: MinIO API Port
  - 9001: MinIO Console Port
- **Image:** minio/minio
- **Volume:** minio-data for persistent storage
- **Command:** Runs MinIO server with custom address configuration

**Key Environment Variables:**
- `MINIO_ROOT_USER`: Root user for MinIO (default: minio)
- `MINIO_ROOT_PASSWORD`: Root password for MinIO (default: minio)

**Service Interactions:**
- Provides S3-compatible API for artifact storage
- Used by tracker-py and web services for storing binary data
- Accessible via MinIO Console for management

**Local vs Production:**
- Local: Uses default credentials and persistent volume
- Production: TBD (deployment details to be documented)

### postgres (Database)

PostgreSQL serves as the primary database for storing application data, traces, and user information.

**Container Details:**
- **Port:** 5432
- **Image:** postgres:latest
- **Volume:** 
  - postgres: Persistent database storage
  - ./web/db: Database initialization scripts
- **Health Check:** Configured with pg_isready

**Key Environment Variables:**
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)

**Service Interactions:**
- Primary data store for web service (through Prisma)
- Stores trace data for tracker-py service
- Includes health monitoring
- Initialized with custom scripts from web/db directory

**Local vs Production:**
- Local: Uses default credentials and initialization scripts
- Production: TBD (deployment details to be documented)

### inngest (Event Processing)

Inngest manages background job processing and event handling for the application.

**Container Details:**
- **Port:** 8288
- **Image:** inngest/inngest:latest
- **Command:** Starts Inngest server pointing to web service's inngest endpoint
- **Dependencies:** Redis for job queue

**Key Environment Variables:**
- `INNGEST_PORT`: Service port (8288)
- `INNGEST_DEV`: Development mode flag
- `INNGEST_REDIS_URI`: Redis connection string
- `INNGEST_SDK_URL`: Web service Inngest endpoint
- `INNGEST_SIGNING_KEY`: Key for request signing
- `INNGEST_EVENT_KEY`: Event processing key

**Service Interactions:**
- Connects to web service for event processing
- Uses Redis as backend for job queue
- Processes background tasks and events
- Provides development-mode UI for job monitoring

**Local vs Production:**
- Local: Uses development mode with local Redis
- Production: TBD (deployment details to be documented)

### redis (Cache and Queue)

Redis provides caching and job queue functionality for the application.

**Container Details:**
- **Port:** 6379
- **Image:** redis:latest
- **Volume:** redis_data for persistent storage
- **Dependencies:** None (base service)

**Service Interactions:**
- Backend for Inngest job queue
- Provides caching capabilities
- Monitored by RedisInsight
- Persistent data storage

**Local vs Production:**
- Local: Uses default configuration with persistent volume
- Production: TBD (deployment details to be documented)

### redisinsight (Redis Monitor)

RedisInsight provides monitoring and management interface for Redis.

**Container Details:**
- **Port:** 5540
- **Image:** redis/redisinsight:latest
- **Volume:** redisinsight for persistent configuration
- **Dependencies:** Redis service

**Service Interactions:**
- Monitors Redis instance
- Provides web UI for Redis management
- Stores monitoring configuration persistently

**Local vs Production:**
- Local: Available on port 5540 for development
- Production: TBD (monitoring strategy to be documented)

## Database and Storage Setup

### Database Schema

The project uses PostgreSQL as its primary database with the following key models:

**Core Models:**
- **Application**: Represents tracked applications
  - UUID-based identification
  - Stores name, description, and URL
  - Tracks creation and update timestamps
  - Has many ApplicationTrackingKeys

- **Trace**: Stores trace data
  - UUID-based identification
  - Links to Application
  - Contains request/response data
  - Manages artifact relationships

- **ArtifactStore**: Manages storage configurations
  - Configures storage endpoints
  - Tracks active status
  - Links to Applications

- **User Management:**
  - User: Core user information
  - Account: OAuth account connections
  - Session: User session management

### Database Configuration

PostgreSQL is configured with the following specifications:
- Database Name: eval_track_development
- Extensions: pgcrypto for UUID generation
- Initialization Scripts: Located in ./web/db/
- Persistent Storage: Mounted volume for data persistence
- Health Monitoring: Configured with pg_isready checks

### Object Storage (MinIO)

MinIO provides S3-compatible object storage with the following setup:
- **API Access:**
  - API Port: 4569
  - Console Port: 9001
  - Root Credentials: Configured via environment variables
- **Storage:**
  - Persistent Volume: minio-data
  - Bucket Management: Through MinIO Console
  - S3-compatible API for artifact storage
- **Integration:**
  - Used by tracker services for artifact storage
  - Accessible through MinIO Console for management
  - Configured with default development credentials

## Authentication and Event Processing

### Authentication System

The application uses a combination of Auth0 and better-auth for authentication:

**Authentication Flow:**
- Uses Auth0 as the primary authentication provider
- Implements better-auth adapter for Prisma integration
- Supports email/password and OAuth authentication
- Manages user sessions with secure token storage

**Key Components:**
- User Management:
  - Email-based authentication
  - OAuth account connections
  - Session tracking with IP and user agent
- Security Features:
  - Token-based authentication
  - Email verification system
  - Secure password storage
  - Session expiration management

**Environment Configuration:**
- `AUTH0_SECRET`: Secret key for Auth0 operations
- `AUTH0_BASE_URL`: Base URL for Auth0 callbacks
- `AUTH0_ISSUER_BASE_URL`: Auth0 issuer URL
- `AUTH0_CLIENT_ID`: Application client ID
- `AUTH0_CLIENT_SECRET`: Application client secret

### Event Processing System

The application uses Inngest for event processing and background job management:

**Event Processing Flow:**
- Events are processed through Inngest service
- Redis backend for job queue management
- Web service integration via API endpoint

**Key Features:**
- Asynchronous job processing
- Event-driven architecture
- Redis-backed queue system
- Development mode UI for monitoring

**Configuration:**
- Base URL: http://web:3000/api/inngest
- Development Mode: Configurable via INNGEST_DEV
- Redis Integration: Uses Redis for job queue
- Signing and Event Keys: Secured with environment variables

**Environment Variables:**
- `INNGEST_BASE_URL`: Service endpoint
- `INNGEST_EVENT_KEY`: Event processing key
- `INNGEST_SIGNING_KEY`: Request signing key
- `INNGEST_DEV`: Development mode flag
- `INNGEST_REDIS_URI`: Redis connection string

## Local Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js with pnpm
- Python 3.8 or higher
- Task CLI (`npm install -g @go-task/cli`)

### Initial Setup

1. Install dependencies:
```bash
# Install web service dependencies
cd web && pnpm install

# Install Python tracker dependencies
cd ../tracker-py && task install-tracker

# Install other language trackers (optional)
cd ../tracker-ts && pnpm install
cd ../tracker-go && go mod download
cd ../tracker-rs && cargo fetch
```

2. Configure environment variables:
- Copy `.env.example` to `.env` in the web directory
- Set required environment variables:
  ```
  DATABASE_URL=postgresql://postgres:postgres@postgres:5432/eval_track_development
  BETTER_AUTH_SECRET=local-sample
  BETTER_AUTH_URL=http://web:3000
  INNGEST_DEV=0
  INNGEST_BASE_URL=http://inngest:8288
  ```

3. Start the development environment:
```bash
docker compose up --build
```

### Default Credentials

**PostgreSQL:**
- User: postgres
- Password: postgres
- Database: eval_track_development
- Port: 5432

**MinIO:**
- Access Key: minio
- Secret Key: minio
- API Port: 4569
- Console Port: 9001
- Console URL: http://localhost:9001

**Redis:**
- Port: 6379
- RedisInsight UI: http://localhost:5540

**Inngest:**
- Development UI: http://localhost:8288
- Event Key: local-sample
- Signing Key: local-sample

### Service URLs

- Web Frontend: http://localhost:3000
- Tracker API: http://localhost:8080
- MinIO Console: http://localhost:9001
- RedisInsight: http://localhost:5540
- Inngest UI: http://localhost:8288

### Development Workflow

1. Make changes to source code
2. Run checks before committing:
   ```bash
   task check-all-tracker  # For Python tracker
   pnpm lint              # For web service
   ```
3. Services with hot reload:
   - web (Next.js frontend)
   - tracker-py (Python tracker)
4. Database changes:
   - Run Prisma migrations: `cd web && pnpm prisma migrate dev`
   - Apply schema changes: `cd web && pnpm prisma generate`

## Production Deployment

TBD - Production deployment details will be documented here.

## Environment Variables

This section lists the required environment variables for each service. Note: Actual values should be obtained from your team's secure configuration management system.

## Monitoring and Observability

Information about monitoring tools and observability setup.
