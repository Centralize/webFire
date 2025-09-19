# (C) 2025 by OPNLAB Development. All rights reserved.
# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build
