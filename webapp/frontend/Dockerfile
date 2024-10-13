FROM node:alpine3.19

COPY package.json package.json
RUN npm install

COPY . .

RUN npm build

FROM nginx:stable-alpine

COPY --from=build /dist /usr/share/nginx/html
COPY --from=build nginx.conf /usr/nginx/conf.d/default.conf

EXPOSE 3000

CMD [ "nginx", "-g", "daemon off;" ]