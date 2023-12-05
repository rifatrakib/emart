FROM node:18-alpine

WORKDIR /shop

COPY package.json ./
RUN npm install
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
