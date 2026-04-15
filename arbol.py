class Nodo:
    def __init__(self, texto, es_hoja=False):
        self.texto = texto
        self.es_hoja = es_hoja
        self.nodo_si = None
        self.nodo_no = None

def crear_arbol_inicial():
    nodo_perro = Nodo("un perro", es_hoja=True)
    nodo_manzana = Nodo("una manzana", es_hoja=True)
    
    raiz = Nodo("¿Es un animal?", es_hoja=False)
    raiz.nodo_si = nodo_perro
    raiz.nodo_no = nodo_manzana
    return raiz

# ==========================================
# MOTOR DE LA INTELIGENCIA ARTIFICIAL
# ==========================================
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
    
    cerebro_raiz = crear_arbol_inicial()
    
    while True:
        print("\n" + "="*40)
        jugar(cerebro_raiz)
        
        jugar_de_nuevo = input("\n¿Quieres jugar otra vez? (s/n): ").lower().strip()
        if jugar_de_nuevo != 's':
            print("¡Hasta la próxima! Guardaré mi conocimiento en mi memoria... (por ahora)")
            break