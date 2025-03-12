from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import spacy

app = Flask(__name__)
nlp = spacy.load("ru_core_news_sm")
tree = ET.parse('bim_model.xml')
root = tree.getroot()

def search_with_ner(query):
    doc = nlp(query)
    floor_num = None
    element_type = None
    
    for token in doc:
        if token.pos_ == "NUM" or token.text.isdigit():
            floor_num = token.text
        elif token.lemma_ in ["перекрытие", "плита", "стена"]:
            element_type = token.lemma_
    
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    results = search_with_ner(query)
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
