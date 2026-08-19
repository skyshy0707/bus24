FROM nginx AS production-stage

WORKDIR /app

#COPY package.json ./
#RUN npm install

RUN apt-get update && apt-get install -y npm

WORKDIR /app
#RUN npm init -y
COPY . .

RUN npm install

ARG VITE_API_HOST
ENV VITE_API_HOST=$VITE_API_HOST

#RUN npm run dev
RUN npm run build