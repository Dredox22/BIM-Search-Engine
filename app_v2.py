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

def load_bim_model(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    bim_dict = {}
    for floor in root.findall(".//floor"):
        floor_num = floor.get("number")
        bim_dict[floor_num] = []
        for elem in floor:
            bim_dict[floor_num].append({
                "id": elem.get("id"),
                "type": elem.get("type"),
                "material": elem.get("material")
            })
    return bim_dict

# Загружаем модель один раз
BIM_MODEL = load_bim_model('bim_model_v2.xml')

def search_bim(query):
    doc = nlp(query.lower())
    floor_num = None
    element_type = None
    material = None
    
    for token in doc:
        if token.text.isdigit():
            floor_num = token.text
        elif token.lemma_ in SYNONYMS:
            element_type = SYNONYMS[token.lemma_]
        elif token.lemma_ in ["бетон", "дерево", "сталь"]:
            material = token.lemma_
    
    results = []
    for floor, elements in BIM_MODEL.items():
        if floor_num and floor != floor_num:
            continue
        for elem in elements:
            if element_type and elem["type"] == element_type:
                if material and elem["material"] != material:
                    continue
                results.append(elem)
    
    return results if results else {"error": "Ничего не найдено"}

# Тесты

print(search_bim("Найди все перекрытия на 3 этаже"))  # Конкретный этаж
print(search_bim("Найди плиты из бетона на 2 этаже"))  # Синоним + материал
print(search_bim("Найди окна на 5 этаже"))  # Ненайденный элемент