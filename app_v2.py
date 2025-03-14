import xml.etree.ElementTree as ET
import spacy

# Загружаем SpaCy для русского языка

nlp = spacy.load("ru_core_news_sm")

# Словарь синонимов

SYNONYMS = {
    "перекрытия": "перекрытие",
    "плиты": "перекрытие",
    "стены": "стена",
    "окна": "окно"
}

# Парсим BIM-модель

tree = ET.parse('bim_model_v2.xml')
root = tree.getroot()

def search_bim(query):
    doc = nlp(query.lower())
    floor_num = None
    element_type = None
    material = None
    
    # Извлекаем сущности
    
    for token in doc:
        if token.text.isdigit():
            floor_num = token.text
        elif token.lemma_ in SYNONYMS:
            element_type = SYNONYMS[token.lemma_]
        elif token.lemma_ in ["бетон", "дерево", "сталь"]:  # Материалы
            material = token.lemma_
    
    # Поиск по дереву
    
    results = []
    for floor in root.findall(".//floor"):
        if floor_num and floor.get("number") != floor_num:
            continue
        for elem in floor:
            if element_type and elem.get("type") == element_type:
                if material and elem.get("material") != material:
                    continue
                results.append({
                    "id": elem.get("id"),
                    "floor": floor.get("number"),
                    "type": elem.get("type"),
                    "material": elem.get("material")
                })
    
    return results if results else {"error": "Ничего не найдено"}

# Тесты

print(search_bim("Найди все перекрытия на 3 этаже"))  # Конкретный этаж
print(search_bim("Найди плиты из бетона на 2 этаже"))  # Синоним + материал
print(search_bim("Найди окна на 5 этаже"))  # Ненайденный элемент