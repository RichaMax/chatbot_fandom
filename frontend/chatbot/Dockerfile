FROM node

WORKDIR /app

COPY package.json .
COPY yarn.lock . 
RUN yarn --frozen-lockfile

COPY . .

EXPOSE 5173

CMD ["yarn", "dev"]