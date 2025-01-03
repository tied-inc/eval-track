FROM node:20-slim

WORKDIR /app

RUN apt-get update -y && apt-get install -y openssl
COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm

RUN pnpm install

COPY . .

EXPOSE 3000

CMD ["pnpm", "build", "&", "pnpm", "start"]