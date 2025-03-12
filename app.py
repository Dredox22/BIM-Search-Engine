import xml.etree.ElementTree as ET

# Парсим XML-файл
tree = ET.parse('bim_model.xml')
root = tree.getroot()

# Простая функция поиска
def simple_search(query):
    results = []
    # Разбиваем запрос на части (простые правила)
    query = query.lower()
    floor_num = None
    element_type = "перекрытие" if "перекрытия" in query else None
    
    # Ищем этаж в запросе
    for word in query.split():
        if word.isdigit():
            floor_num = word
    
    # Поиск по дереву
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
result = simple_search(query)
print(result)
# Вывод: [{'id': 'slab_3', 'floor': '3', 'type': 'перекрытие', 'material': 'concrete'}]
