import json
import os

ARCHIVO_CEREBRO = "cerebro.json"

def cargar_conocimiento():
    """Carga la matriz de objetos y preguntas."""
    if os.path.exists(ARCHIVO_CEREBRO):
        with open(ARCHIVO_CEREBRO, 'r', encoding='utf-8') as f:
            return json.load(f)
    print("⚠️ Error: No se encontró el cerebro.json con la matriz de datos.")
    return {"objetos": {}, "preguntas": {}}

def guardar_conocimiento(datos):
    """Guarda la matriz actualizada en el disco."""
    with open(ARCHIVO_CEREBRO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Memoria matricial actualizada y guardada. 💾")

def jugar():
    datos = cargar_conocimiento()
    objetos = datos.get("objetos", {})
    preguntas = datos.get("preguntas", {})
    
    if not objetos or not preguntas:
        return

    # 1. ESTADO INICIAL: Todos los objetos comienzan con 0 puntos de probabilidad
    puntajes = {nombre: 0.0 for nombre in objetos.keys()}
    
    print("\n" + "="*40)
    print("Responde con: 's' (Sí), 'n' (No) o 't' (Tal vez)")
    print("="*40)
    
    # 2. FASE DE NAVEGACIÓN (Cálculo de pesos)
    for id_preg, texto_preg in preguntas.items():
        respuesta = input(f"{texto_preg} (s/n/t): ").lower().strip()
        
        # Ajustamos los puntajes de TODOS los objetos según la respuesta
        for obj_nombre, atributos in objetos.items():
            # Si la IA no sabe la relación de este objeto con la pregunta, asume 0 (Neutral)
            peso_atributo = atributos.get(id_preg, 0.0) 
            
            if respuesta == 's':
                puntajes[obj_nombre] += peso_atributo     # Suma si el rasgo coincide
            elif respuesta == 'n':
                puntajes[obj_nombre] -= peso_atributo     # Resta si el rasgo es opuesto
            # Si la respuesta es 't' (tal vez), el puntaje no cambia (se suma 0)

    # 3. FASE DE ADIVINACIÓN
    # Ordenamos los objetos de mayor a menor puntuación
    ranking = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    mejor_opcion = ranking[0][0] # Tomamos el nombre del primer lugar
    
    # (Opcional) Imprimir el Top 3 para ver cómo pensó la IA
    # print(f"DEBUG - Top 3: {ranking[:3]}") 
    
    print("\n" + "-"*40)
    respuesta_final = input(f"¿Estás pensando en {mejor_opcion}? (s/n): ").lower().strip()
    
    if respuesta_final == 's':
        print("¡La probabilidad matemática nunca falla! He ganado. 🤖🏆")
    else:
        # 4. FASE DE APRENDIZAJE MATRICIAL
        print("¡Vaya! La entropía me ha superado. Ayúdame a aprender.")
        nuevo_obj = input("¿En qué estabas pensando? (ej: un avión): ").lower().strip()
        
        if nuevo_obj not in objetos:
            objetos[nuevo_obj] = {} # Creamos el objeto vacío
            
        nueva_preg_texto = input(f"Escribe una pregunta de Sí/No que sea VERDADERA para '{nuevo_obj}' pero FALSA para '{mejor_opcion}':\n> ")
        
        # Creamos un ID único para la nueva pregunta (ej: "preg_6")
        id_nueva_preg = f"preg_{len(preguntas) + 1}"
        preguntas[id_nueva_preg] = nueva_preg_texto
        
        # Asignamos los pesos extremos (+1 y -1) para separar ambos objetos en el futuro
        objetos[nuevo_obj][id_nueva_preg] = 1.0
        objetos[mejor_opcion][id_nueva_preg] = -1.0
        
        print("¡Conocimiento matricial expandido! 🧠✨")
        guardar_conocimiento(datos)

if __name__ == "__main__":
    print("--- MOTOR IA: SISTEMA DE PROBABILIDAD (TIPO 20Q) ---")
    while True:
        jugar()
        if input("\n¿Quieres jugar otra vez? (s/n): ").lower().strip() != 's':
            print("Apagando red neuronal... ¡Hasta pronto!")
            break