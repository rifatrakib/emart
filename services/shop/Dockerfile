FROM node:alpine

WORKDIR /shop

COPY package*.json ./
RUN npm install

COPY . .
# RUN npm run build
# RUN npm prune --production

EXPOSE 3000
CMD ["npm", "start"]
