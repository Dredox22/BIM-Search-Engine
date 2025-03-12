# Базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код и данные
COPY app.py .
COPY bim_model.xml .

# Запускаем приложение
CMD ["python", "app.py"]