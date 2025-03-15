import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
import numpy as np

# Загружаем модель
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

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

# Подготовка данных
BIM_MODEL = load_bim_model('bim_model_v2.xml')
element_descriptions = []
element_metadata = []
for floor, elements in BIM_MODEL.items():
    for elem in elements:
        desc = f"{elem['type']} на этаже {floor}, материал {elem['material']}"
        element_descriptions.append(desc)
        element_metadata.append(elem)

# Векторизуем элементы
element_vectors = model.encode(element_descriptions)

def vector_search(query):
    query_vector = model.encode([query])[0]
    similarities = np.dot(element_vectors, query_vector) / (np.linalg.norm(element_vectors, axis=1) * np.linalg.norm(query_vector))
    top_indices = similarities.argsort()[-3:][::-1]  # Топ-3 результата
    results = [element_metadata[i] for i in top_indices if similarities[i] > 0.5]  # Порог сходства
    return results if results else {"error": "Ничего не найдено"}

# Тест
print(vector_search("Найди перекрытия из бетона на 3 этаже"))
print(vector_search("Потолки на втором этаже"))