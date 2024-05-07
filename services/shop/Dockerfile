FROM node:current-slim

WORKDIR /services/shop

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build
EXPOSE 8080

CMD npm run start
