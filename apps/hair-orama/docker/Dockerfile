# Use the Node.js 18 Alpine image as the base image
FROM node:18-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4200

# Command to serve the Angular application with NX
# CMD ["npx", "nx", "serve", "hair-orama"]
CMD ["npx", "nx", "serve", "hair-orama", "--host", "0.0.0.0"]

