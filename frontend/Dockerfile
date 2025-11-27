# ============================================================================
# Frontend Dockerfile - React Application
# ============================================================================
# Multi-stage build:
# Stage 1: Build the React application with Node.js
# Stage 2: Serve static files with Nginx
# ============================================================================


# ============================================================================
# Stage 1: Build Stage
# ============================================================================
FROM node:20-alpine as build


# Set working directory
WORKDIR /app


# Copy package files
COPY package*.json ./


# Install dependencies
RUN npm install


# Copy source code
COPY . .


# Build argument for API URL (can be overridden at build time)
# Default is '/api' which works as a relative URL in all environments
# Local: /api -> proxied to backend by Nginx
# AWS: /api -> handled by your reverse proxy or API Gateway
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL


# Build the application
RUN npm run build


# ============================================================================
# Stage 2: Production Stage with Nginx
# ============================================================================
FROM nginx:alpine


# Install curl for health checks
RUN apk add --no-cache curl


# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf


# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html


# Expose port 80
EXPOSE 80


# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD curl -f http://localhost/health || exit 1


# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
