# frontend/Dockerfile

# Sử dụng Node.js phiên bản 20 từ Docker Hub
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build ứng dụng
RUN npm run build

# Expose cổng 3000 cho frontend ReactJS
EXPOSE 3000

# Serve ứng dụng sử dụng serve
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
