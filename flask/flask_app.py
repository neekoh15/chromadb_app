"""
API REST en Flask
Instrucciones para Windows:
1. Instalar waitress: pip install waitress
2. Ejecutar la aplicación: waitress-serve --port=3000 app:app

@autor: Martinez, Nicolas Agustin
"""
# Importación de módulos necesarios

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import webbrowser, chromadb

# Inicialización de la aplicación Flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crm')
def pagina2():
    return render_template('crm.html')


@app.route('/abc_consultas_frecuentes', methods=['POST'])
def query_abc():
    """
    Endpoint para obtener similitudes basadas en el texto proporcionado.
    
    Entrada: JSON con el campo 'text'
    Salida: JSON con las similitudes encontradas o un objeto JSON vacío en caso de error

    
    """
    collection_name = 'abc_collection'
    collection = client.get_collection(collection_name)
    
    # Obtener datos del cuerpo de la solicitud
    #data:dict = request.json
    #print('DENTRO DE query_abc() EN APP.py')
    data = request.form
    print(data)
    # Si no hay datos, retornar None
    if not data:
        return None
    
    # Extraer el texto del JSON
    pregunta:str = data['pregunta']

    # Intentar obtener similitudes y devolver la respuesta
    try:
        response:chromadb.QueryResult = collection.query(
            query_texts=pregunta, 
            n_results=5,
            include=['documents', 'metadatas', 'distances'])
        
        #return response
        print(response)
        return jsonify(response)
    
    except Exception as e:
        # Imprimir el error y devolver un objeto JSON vacío
        print('Error al obtener similitudes:', e)
        return {}

@app.route('/crm_respuestas', methods=["POST"])
def query_crm():
    """
    Endpoint para obtener similitudes basadas en el texto proporcionado.
    
    Entrada: form con el campo 'pregunta'
    Salida: JSON con las similitudes encontradas o un objeto JSON vacío en caso de error
    
    """
    collection_name = 'crm_collection'
    collection = client.get_collection(collection_name)

    # Inicialización de la conexion a la base de datos

    # Obtener datos del cuerpo de la solicitud
    #data:dict = request.json
    print('DENTRO DE query_crm() EN APP.py')
    data = request.form
    #print(data)
    # Si no hay datos, retornar None
    if not data:
        return None
    
    # Extraer el texto del JSON
    pregunta:str = data['pregunta']

    # Intentar obtener similitudes y devolver la respuesta
    try:
        response:chromadb.QueryResult = collection.query(
            query_texts=pregunta,
            n_results=5,
            include=['documents', 'metadatas'])

        print('RESPUESTA DESDE SERVIDOR: ', response)
        #return response
        return jsonify(response)
    
    except Exception as e:
        # Imprimir el error y devolver un objeto JSON vacío
        print('Error al obtener similitudes:', e)
        return {}


@app.route('/monotributo_respuestas', methods=["POST"])
def query_monotributo():
    """
    Endpoint para obtener similitudes basadas en el texto proporcionado.
    
    Entrada: form con el campo 'pregunta'
    Salida: JSON con las similitudes encontradas o un objeto JSON vacío en caso de error
    
    """

    
    collection_name = 'monotributo_collection'
    collection = client.get_collection(collection_name)

    
    # Obtener datos del cuerpo de la solicitud
    #data:dict = request.json
    print('DENTRO DE query_crm() EN APP.py')
    data = request.form
    print(data)
    # Si no hay datos, retornar None
    if not data:
        return None
    
    # Extraer el texto del JSON
    pregunta:str = data['pregunta']

    # Intentar obtener similitudes y devolver la respuesta
    try:
        response:chromadb.QueryResult = collection.query(
            query_texts=pregunta, 
            n_results=5,
            include=['metadatas', 'documents'])

        print('RESPUESTA DESDE SERVIDOR: ', response)
        #return response
        return jsonify(response)
    
    except Exception as e:
        # Imprimir el error y devolver un objeto JSON vacío
        print('Error al obtener similitudes:', e)
        return {}



@app.route('/get_links', methods=['POST'])
def get_links():

    collection_name = 'links_respuestas'
    database_name = 'links_database'

    # Inicialización de la conexion a la base de datos
    #db = CRM_DataBase()
    #db.connect(database_name=database_name)
    #db.set_collection(collection_name=collection_name)
    
    # Obtener datos del cuerpo de la solicitud
    #data:dict = request.json
    print('DENTRO DE query_crm() EN APP.py')
    data = request.json 
    print(data)
    # Si no hay datos, retornar None
    if not data:
        return None
    
    # Extraer el texto del JSON
    pregunta:str = data['pregunta']

    # Intentar obtener similitudes y devolver la respuesta
    try:
        response:dict = db.query(query=pregunta, n_results=5)

        print('RESPUESTA DESDE SERVIDOR: ', response)
        #return response
        return jsonify(response)
    
    except Exception as e:
        # Imprimir el error y devolver un objeto JSON vacío
        print('Error al obtener similitudes:', e)
        return {}

@app.route('/update_crm', methods=["POST"])
def update_crm():
    data = request.get_json()
    id = data['id']
    metadata = data['metadata']

    collection_name = 'crm_respuestas'
    database_name = 'crm_database'

    # Inicialización de la conexion a la base de datos
    db = CRM_DataBase()
    db.connect(database_name=database_name)
    db.set_collection(collection_name=collection_name)

    db.update_collection(id=id, metadata=metadata)
    return 'NUEVO VALOR AGREGADO A LA BASE DE DATOS'


if __name__ == '__main__':
    webbrowser.open('http://localhost:5500')

    client = chromadb.HttpClient()
    # Habilitación de CORS para la aplicación

    CORS(app)

    # (Opcional) Para montar la API en línea, descomentar la siguiente línea
    # run_with_ngrok(app)

    app.run(host='localhost', port=5500, debug=True)
