import json
import os

class Nodo:
    def __init__(self, texto, es_hoja=False):
        self.texto = texto
        self.es_hoja = es_hoja
        self.nodo_si = None
        self.nodo_no = None

# GESTIÓN DE MEMORIA
def nodo_a_diccionario(nodo):
    """Convierte un Nodo (y todos sus hijos) en un diccionario de Python recursivamente."""
    if nodo is None:
        return None
    
    return {
        "texto": nodo.texto,
        "es_hoja": nodo.es_hoja,
        "nodo_si": nodo_a_diccionario(nodo.nodo_si),
        "nodo_no": nodo_a_diccionario(nodo.nodo_no)
    }

def diccionario_a_nodo(datos):
    """Convierte un diccionario de Python de vuelta en un árbol de Nodos recursivamente."""
    if datos is None:
        return None
    
    nodo = Nodo(datos["texto"], datos["es_hoja"])
    nodo.nodo_si = diccionario_a_nodo(datos["nodo_si"])
    nodo.nodo_no = diccionario_a_nodo(datos["nodo_no"])
    return nodo

def guardar_conocimiento(raiz, archivo="cerebro.json"):
    """Guarda el árbol completo en el disco duro."""
    diccionario_arbol = nodo_a_diccionario(raiz)
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(diccionario_arbol, f, ensure_ascii=False, indent=4)
    print("Conocimiento guardado exitosamente. 💾")

def cargar_conocimiento(archivo="cerebro.json"):
    """Intenta cargar el árbol desde el disco duro. Si no existe, crea el árbol base."""
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        print("He recuperado mis memorias de la sesión anterior. 🧠")
        return diccionario_a_nodo(datos)
    else:
        print("Iniciando con memoria en blanco (Conocimiento Base). 👶")
        return crear_arbol_inicial()

def crear_arbol_inicial():
    nodo_perro = Nodo("un perro", es_hoja=True)
    nodo_manzana = Nodo("una manzana", es_hoja=True)
    
    raiz = Nodo("¿Es un animal?", es_hoja=False)
    raiz.nodo_si = nodo_perro
    raiz.nodo_no = nodo_manzana
    return raiz

# MOTOR DE LA INTELIGENCIA ARTIFICIAL
def jugar(nodo_actual):
    # 1. Fase de Navegación: Bajamos por el árbol hasta llegar a una hoja
    while not nodo_actual.es_hoja:
        respuesta = input(f"{nodo_actual.texto} (s/n): ").lower().strip()
        if respuesta == 's':
            nodo_actual = nodo_actual.nodo_si
        elif respuesta == 'n':
            nodo_actual = nodo_actual.nodo_no
        else:
            print("Por favor, responde solo con 's' (Sí) o 'n' (No).")

    # 2. Fase de Adivinación: Hemos llegado a una hoja
    respuesta_final = input(f"¿Estás pensando en {nodo_actual.texto}? (s/n): ").lower().strip()
    
    if respuesta_final == 's':
        print("¡Jaja! ¡La Inteligencia Artificial gana de nuevo! 🤖🏆")
    else:
        # 3. Fase de Aprendizaje: La IA se equivocó y necesita crecer
        print("Vaya, me has ganado. ¡Ayúdame a aprender!")
        nuevo_elemento = input("¿En qué estabas pensando? (ej: un gato): ").lower().strip()
        nueva_pregunta = input(f"Escribe una pregunta de Sí/No para distinguir '{nuevo_elemento}' de '{nodo_actual.texto}':\n> ")
        respuesta_nuevo = input(f"Para '{nuevo_elemento}', ¿la respuesta a esa pregunta es 's' o 'n'?: ").lower().strip()

        # Transformamos la hoja actual en una nueva rama (pregunta)
        viejo_texto = nodo_actual.texto
        nodo_actual.texto = nueva_pregunta
        nodo_actual.es_hoja = False

        # Conectamos las nuevas hojas a esta rama
        if respuesta_nuevo == 's':
            nodo_actual.nodo_si = Nodo(nuevo_elemento, es_hoja=True)
            nodo_actual.nodo_no = Nodo(viejo_texto, es_hoja=True)
        else:
            nodo_actual.nodo_no = Nodo(nuevo_elemento, es_hoja=True)
            nodo_actual.nodo_si = Nodo(viejo_texto, es_hoja=True)
        
        print("¡Gracias! He expandido mi conocimiento. 🧠✨")

# --- BUCLE PRINCIPAL ---
if __name__ == "__main__":
    print("--- BIENVENIDO AL ORÁCULO DE LAS 20 PREGUNTAS ---")
    print("Piensa en algo y yo intentaré adivinarlo.")
    
    # 1. Cargamos la memoria en lugar de crearla de cero
    cerebro_raiz = cargar_conocimiento()
    
    while True:
        print("\n" + "="*40)
        jugar(cerebro_raiz)
        
        jugar_de_nuevo = input("\n¿Quieres jugar otra vez? (s/n): ").lower().strip()
        if jugar_de_nuevo != 's':
            # 2. Guardamos la memoria antes de cerrar
            print("¡Hasta la próxima! Guardando mis memorias en el disco duro...")
            guardar_conocimiento(cerebro_raiz)
            break