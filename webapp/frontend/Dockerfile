FROM node:alpine3.19 AS build

COPY package.json package.json
RUN npm install

COPY . .

RUN npm run build

FROM nginx:stable-alpine

COPY --from=build ./build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD [ "nginx", "-g", "daemon off;" ]