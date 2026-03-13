FROM node:20.19-alpine

WORKDIR /app

# Copier les fichiers de dependances
COPY package.json package-lock.json* ./

# Installer les dependances
RUN npm install

# Copier le reste du projet
COPY . .

# Build pour production
RUN npm run build

# Port Next.js
EXPOSE 3000

# Lancer en mode production
CMD ["npm", "start"]
