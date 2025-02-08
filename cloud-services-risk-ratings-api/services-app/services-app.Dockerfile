# Stage 1: Build the React app
FROM node:20 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Serve the app with Node.js
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install only production dependencies
RUN npm install --only=production

# Copy the build from the previous stage
COPY --from=build /app/build ./build
COPY server.js ./
COPY certs ./certs

# Set permissions for certs
RUN chmod 400 /app/certs/server8186.key /app/certs/server8186.cert

# Expose the port that the Node.js app will run on
EXPOSE 8186

# Define the command to run the application
CMD ["node", "server.js"]