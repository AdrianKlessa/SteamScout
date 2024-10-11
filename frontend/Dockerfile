FROM node:20-alpine AS build-stage
WORKDIR /app
COPY package.json .
ARG VITE_APP_BACKEND_ADDRESS
ENV VITE_APP_BACKEND_ADDRESS $VITE_APP_BACKEND_ADDRESS
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.27.2-alpine-slim as prod
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf  /etc/nginx/conf.d
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]