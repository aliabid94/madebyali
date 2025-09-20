FROM node:18-slim AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY tailwind.config.js ./
COPY src/ ./src/
COPY static/ ./static/
COPY pages/ ./pages/

RUN npm run build-css-prod

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=build-stage /app/static/styles.css ./static/styles.css

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]