# Docker Quick Start Guide

## 🐳 Quick Commands

### Using Docker Compose (Easiest)

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

Access:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Using Build Script

Make the script executable (Linux/Mac):
```bash
chmod +x docker-build.sh
```

Run commands:
```bash
# Build both images
./docker-build.sh build

# Start services
./docker-build.sh up

# View logs
./docker-build.sh logs

# Stop services
./docker-build.sh down

# Clean up
./docker-build.sh clean
```

### Manual Docker Commands

#### Backend Only
```bash
# Build
docker build -f Dockerfile.backend -t taskmanager-backend .

# Run
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  --name taskmanager-backend \
  taskmanager-backend

# View logs
docker logs -f taskmanager-backend

# Stop
docker stop taskmanager-backend
docker rm taskmanager-backend
```

#### Frontend Only
```bash
# Build
docker build -f Dockerfile.frontend -t taskmanager-frontend .

# Run
docker run -d \
  -p 80:80 \
  --name taskmanager-frontend \
  taskmanager-frontend

# View logs
docker logs -f taskmanager-frontend

# Stop
docker stop taskmanager-frontend
docker rm taskmanager-frontend
```

## 🔧 Environment Variables

Create a `.env` file in the project root:

```env
# Backend
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=sqlite:////app/data/task_manager.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend (build-time)
VITE_API_URL=http://localhost:8000
```

Generate secure SECRET_KEY:
```bash
# Using OpenSSL
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📦 Docker Images

### Backend Image Details
- Base: `python:3.10-slim`
- Size: ~200MB
- Port: 8000
- Health check: `GET /health`

### Frontend Image Details
- Base: `nginx:alpine`
- Size: ~50MB
- Port: 80
- Serves static files
- React Router support

## 🔍 Debugging

### Check if containers are running
```bash
docker ps
```

### View container logs
```bash
docker logs taskmanager-backend
docker logs taskmanager-frontend
```

### Execute commands in container
```bash
# Backend
docker exec -it taskmanager-backend bash
docker exec -it taskmanager-backend python -c "from app.database import init_db; init_db()"

# Frontend
docker exec -it taskmanager-frontend sh
```

### Check container health
```bash
docker inspect taskmanager-backend | grep -A 10 Health
docker inspect taskmanager-frontend | grep -A 10 Health
```

### Test backend API
```bash
curl http://localhost:8000/health
curl http://localhost:8000/
```

## 🧹 Cleanup Commands

### Remove stopped containers
```bash
docker container prune
```

### Remove unused images
```bash
docker image prune -a
```

### Remove volumes
```bash
docker volume prune
```

### Remove everything (nuclear option)
```bash
docker system prune -a --volumes
```

### Stop and remove specific containers
```bash
docker-compose down -v
```

## 📊 Monitoring

### View resource usage
```bash
docker stats
```

### View container details
```bash
docker inspect taskmanager-backend
docker inspect taskmanager-frontend
```

### Check network
```bash
docker network ls
docker network inspect taskmanager-network
```

## 🚨 Common Issues

### Port already in use
```bash
# Find process using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Use different port
docker run -p 8001:8000 taskmanager-backend
```

### Permission denied
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER

# Or run with sudo
sudo docker-compose up
```

### Container exits immediately
```bash
# Check logs
docker logs taskmanager-backend

# Run in foreground to see errors
docker-compose up
```

### Database locked
```bash
# Remove volume and restart
docker-compose down -v
docker-compose up -d
```

### Build fails
```bash
# Clear build cache
docker builder prune

# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

## 🎯 Production Tips

1. **Use proper secret key**:
   ```bash
   export SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **Use PostgreSQL instead of SQLite**:
   - Add PostgreSQL to docker-compose.yml
   - Update DATABASE_URL
   - More reliable for production

3. **Add reverse proxy**:
   - Use Traefik or Caddy
   - Automatic HTTPS
   - Load balancing

4. **Enable logging**:
   - Configure log drivers
   - Send logs to external service
   - Monitor application health

5. **Set resource limits**:
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '0.5'
             memory: 512M
   ```

## 📚 Next Steps

- Read `RAILWAY_DEPLOYMENT.md` for Railway deployment
- Check `FULL_PROJECT_GUIDE.md` for complete documentation
- Review docker-compose.yml for configuration options

---

**Happy Dockerizing! 🐳**
