FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Install serve to run production build
RUN npm install -g serve

# Run application
CMD ["serve", "-s", "dist", "-l", "3000"]
