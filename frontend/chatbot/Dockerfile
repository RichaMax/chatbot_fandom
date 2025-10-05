FROM node

WORKDIR /app

RUN npm install vite

COPY package.json .
COPY yarn.lock . 
RUN yarn --frozen-lockfile

COPY . .

EXPOSE 5173

CMD ["yarn", "dev"]
