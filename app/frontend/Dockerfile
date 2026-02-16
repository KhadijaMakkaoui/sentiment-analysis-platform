# Use Node.js for building and running
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the port React runs on
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]