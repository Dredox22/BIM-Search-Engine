# BIM Search Engine

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Описание проекта

**BIM Search Engine** — это поисковик для строительной отрасли, который принимает запросы на естественном языке (например, "Найди бетонные перекрытия на южной стороне 3 этажа") и возвращает соответствующие элементы из BIM-модели (Building Information Modeling), представленной в виде XML-подобной структуры. Проект демонстрирует интеграцию современных методов NLP (Natural Language Processing), машинного обучения и DevOps для создания масштабируемого и удобного инструмента.

### Основные возможности

- **Анализ запросов:** Извлечение сущностей (этаж, тип элемента, материал, ориентация) с помощью дообученной модели NER (DeepPavlov + LoRA).
- **Семантический поиск:** Векторный поиск по элементам BIM с использованием FAISS для скорости и точности.
- **Генерация ответов:** Русскоязычные текстовые ответы через RAG (Retrieval-Augmented Generation) с моделью `sberbank-ai/rugpt3medium`.
- **Интерфейс:** REST API на Flask, доступный через Docker.
- **Тестирование:** Полное покрытие юнит-тестами с `pytest`.

### Пример использования

- **Запрос:** `curl -X POST -d '{"query":"бетонные перекрытия на 3 этаже"}' http://localhost:5000/search`
- **Ответ:**

  ``` json
  
  {
    "results": [{"id": "slab_4", "type": "перекрытие", "floor": "3", "material": "concrete", "orientation": "east"}],
    "generated_response": "Ответ на русском: Найдено бетонное перекрытие с ID slab_4 на 3 этаже, ориентация восток."
  }
