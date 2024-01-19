# build stage
FROM node:20-alpine3.17 as build-stage
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# dev
#FROM node:20-alpine3.17
#WORKDIR /app
#COPY package.json .
#RUN npm install
#COPY . .
#EXPOSE 80
#CMD ["npm", "run", "dev"]