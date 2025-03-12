import xml.etree.ElementTree as ET
import spacy

# Загружаем модель для русского языка
nlp = spacy.load("ru_core_news_sm")

# Парсим XML
tree = ET.parse('bim_model.xml')
root = tree.getroot()

# Функция поиска с NER
def search_with_ner(query):
    doc = nlp(query)
    floor_num = None
    element_type = None
    
    # Извлекаем сущности и ключевые слова
    for token in doc:
        if token.pos_ == "NUM" or token.text.isdigit():  # Число (этаж)
            floor_num = token.text
        elif token.lemma_ in ["перекрытие", "плита", "стена"]:  # Тип элемента
            element_type = token.lemma_
    
    # Поиск по дереву
    results = []
    for floor in root.findall(".//floor"):
        if floor_num and floor.get("number") != floor_num:
            continue
        for elem in floor:
            if element_type and elem.get("type") == element_type:
                results.append({
                    "id": elem.get("id"),
                    "floor": floor.get("number"),
                    "type": elem.get("type"),
                    "material": elem.get("material")
                })
    
    return results

# Тест
query = "Найди все перекрытия на 3 этаже"
result = search_with_ner(query)
print(result)
# Вывод: [{'id': 'slab_3', 'floor': '3', 'type': 'перекрытие', 'material': 'concrete'}]
