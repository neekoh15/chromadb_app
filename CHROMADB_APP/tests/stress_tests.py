
import chromadb
import time, importlib
import matplotlib.pyplot as plt



def iter_test(intervalos:list=[], f=None):
    
    promedios = []
    
    for amount in intervalos:
        promedio = f(amount)
        promedios.append(promedio)
        
    else:
        plt.plot(intervalos, promedios)
        plt.xlabel('Cantidad de queries')
        plt.ylabel('Queries por segundo [q/seg]')
        plt.grid(visible=True)
        plt.title('Caudal de queries vs Total queries')
        plt.show()
        

def stress_test1(query_amout:int, collection_name:str=None, query_text:str=None) -> None:

    print(' Comenzando prueba de stress: stress_test1')
    print('Cantidad de queries a realizar: ', query_amout)

    # si no se especifica una coleccion, se selecciona la primer coleccion dentro de la base de datos 
    if not collection_name:

        #print('Client collections: ', client.list_collections())
        collections:dict = client.list_collections()
        collection:chromadb.Collection = collections[0]
        collection_name:str = collection.name
        
    t_i = time.perf_counter()
    for _ in range(query_amout):
        collection.query(
            query_texts= 'default_query' if not query_text else query_text,
            n_results= 2
            )
        
    else:
        t_total = (time.perf_counter() - t_i) # pasaje de microsegundos a milisegundos
        promedio = query_amout/t_total
        print(f'se han realizado {query_amout} consultas en {t_total:.4f} segundos.')
        print(f'Cantidad de consultas por segundo: {promedio:.4f}')
  
        return promedio
    
def concurrency_test1():
    pass
        
if __name__ == '__main__':

    client = None

    try:
        print('Intentando alcanzar el servidor de base de datos')
        client = chromadb.HttpClient()
        print('Conexion a la base de datos remota exitosa. \n')
    except Exception as e:
        print('No se pudo alcanzar el servidor local.', e)

    try:
        print('Intentando alcanzar la base de datos persistente')
        client = chromadb.PersistentClient('./database')
        print('Conexion a la base de datos persistente exitosa. \n')
    except Exception as e:
        print('No se pudo alcanzar la base de datos persistente.', e)

    
    if client:
            iter_test(f=stress_test1, intervalos=[10, 20, 30, 50, 100])
