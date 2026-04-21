import json
import os
import requests
import random

ARCHIVO_CEREBRO = "cerebro.json"

# ==========================================
# GESTIÓN DE MEMORIA
# ==========================================
def cargar_conocimiento():
    """Carga la matriz de objetos y preguntas desde el disco."""
    if os.path.exists(ARCHIVO_CEREBRO):
        with open(ARCHIVO_CEREBRO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"objetos": {}, "preguntas": {}}

def guardar_conocimiento(datos):
    """Guarda la matriz actualizada en el disco."""
    with open(ARCHIVO_CEREBRO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Memoria matricial actualizada y guardada. 💾")

# ==========================================
# CONEXIÓN A LA MATRIX (CONCEPTNET)
# ==========================================
def consultar_conceptnet(palabra):
    """Busca atributos de una palabra en Internet usando ConceptNet API."""
    # Limpiamos la palabra para que la API la entienda mejor
    palabra_limpia = palabra.replace("un ", "").replace("una ", "").replace("el ", "").replace("la ", "").replace(" ", "_")
    print(f"\n🌐 [Conectando a la red global para investigar: '{palabra_limpia}']...")
    
    url = f"https://api.conceptnet.io/c/es/{palabra_limpia}?limit=30"
    
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            for edge in datos.get('edges', []):
                relacion = edge['rel']['label']
                destino = edge['end']['label']
                idioma_destino = edge['end'].get('language', '')
                
                if idioma_destino == 'es':
                    # Transformamos la relación de la API en una pregunta humana
                    if relacion == "IsA": return f"¿Es un/una {destino}?"
                    elif relacion == "CapableOf": return f"¿Es capaz de {destino}?"
                    elif relacion == "HasA": return f"¿Tiene {destino}?"
                    elif relacion == "UsedFor": return f"¿Se usa para {destino}?"
                    elif relacion == "AtLocation": return f"¿Suele encontrarse en {destino}?"
        return None # No encontró relaciones útiles en español
    except requests.RequestException:
        print("⚠️ [Error de conexión: La Matrix está caída o inaccesible]")
        return None

# ==========================================
# BUCLE PRINCIPAL DEL JUEGO
# ==========================================
def jugar():
    datos = cargar_conocimiento()
    objetos = datos.get("objetos", {})
    preguntas = datos.get("preguntas", {})
    
    if not objetos or not preguntas:
        print("El cerebro está vacío. Asegúrate de tener tu cerebro.json inicial.")
        return

    # 1. ESTADO INICIAL: Todos los objetos empiezan en 0
    puntajes = {nombre: 0.0 for nombre in objetos.keys()}
    
    print("\n" + "="*50)
    print("Responde con: 's' (Sí), 'n' (No) o 't' (Tal vez)")
    print("="*50)
    
    # 2. FASE DE NAVEGACIÓN (Cálculo de probabilidades y Umbral de Confianza)
    preguntas_hechas = 0
    limite_preguntas = 20 # ¡El nombre del juego!
    
    for id_preg, texto_preg in preguntas.items():
        if preguntas_hechas >= limite_preguntas:
            print("\n⏳ He alcanzado mi límite de preguntas. Intentaré adivinar.")
            break
            
        respuesta = input(f"[{preguntas_hechas + 1}] {texto_preg} (s/n/t): ").lower().strip()
        preguntas_hechas += 1
        
        # Ajustamos los puntajes
        for obj_nombre, atributos in objetos.items():
            peso_atributo = atributos.get(id_preg, 0.0) 
            if respuesta == 's': puntajes[obj_nombre] += peso_atributo
            elif respuesta == 'n': puntajes[obj_nombre] -= peso_atributo
            
        # --- EL SENSOR DE CONFIANZA ---
        # Ordenamos a los competidores en tiempo real
        ranking_temporal = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
        
        # Necesitamos al menos 2 objetos para comparar
        if len(ranking_temporal) >= 2:
            primer_lugar = ranking_temporal[0][1]
            segundo_lugar = ranking_temporal[1][1]
            
            # Si el primer lugar le lleva 2.0 puntos de ventaja al segundo, ¡la IA ya está segura!
            if (primer_lugar - segundo_lugar) >= 2.0:
                print("\n💡 ¡Lo tengo claro! Mi red neuronal ya sabe la respuesta.")
                break # Rompemos el bucle prematuramente

    # 3. FASE DE ADIVINACIÓN
    ranking = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    mejor_opcion = ranking[0][0]
    
    print("\n" + "-"*50)
    respuesta_final = input(f"¿Estás pensando en {mejor_opcion}? (s/n): ").lower().strip()
    
    if respuesta_final == 's':
        print("¡La probabilidad matemática nunca falla! He ganado. 🤖🏆")
    else:
        # 4. FASE DE APRENDIZAJE Y SUPERVIVENCIA
        print("¡Vaya! La entropía me ha superado. Voy a investigar.")
        nuevo_obj = input("¿En qué estabas pensando? (ej: perro, avion, guitarra): ").lower().strip()
        
        if nuevo_obj not in objetos:
            objetos[nuevo_obj] = {}
            
        nueva_preg_texto = None
        id_nueva_preg = None
        
        # --- PLAN A: INTERNET ---
        pregunta_internet = consultar_conceptnet(nuevo_obj)
        if pregunta_internet:
            print(f"💡 [PLAN A] ConceptNet sugiere: '{pregunta_internet}'")
            if input("¿Es correcta esta pregunta para distinguirlos? (s/n): ").lower().strip() == 's':
                nueva_preg_texto = pregunta_internet
                id_nueva_preg = f"preg_{len(preguntas) + 1}"
                preguntas[id_nueva_preg] = nueva_preg_texto

        # --- PLAN B: RECICLAJE LOCAL ---
        if not nueva_preg_texto and len(preguntas) > 0:
            print("\n🧠 [PLAN B] Buscando en mi memoria local...")
            preguntas_conocidas = list(preguntas.items())
            random.shuffle(preguntas_conocidas)
            
            intentos = 0
            for id_preg, texto_preg in preguntas_conocidas:
                if intentos >= 3: break # Máximo 3 intentos para no frustrar al jugador
                
                peso_perdedor = objetos[mejor_opcion].get(id_preg, 0.0)
                if peso_perdedor != 0.0:
                    print(f"¿Podríamos usar esta pregunta?: '{texto_preg}'")
                    resp = input(f"Para '{nuevo_obj}', la respuesta es (s/n/t): ").lower().strip()
                    if resp != 't':
                        print("¡Perfecto! Reciclaré esta pregunta.")
                        id_nueva_preg = id_preg
                        nueva_preg_texto = texto_preg
                        # Ajustamos el peso para el nuevo objeto según lo que respondió el usuario
                        objetos[nuevo_obj][id_nueva_preg] = 1.0 if resp == 's' else -1.0
                        break
                    intentos += 1

        # --- PLAN C: MODO MANUAL ---
        if not nueva_preg_texto:
            print("\n📝 [PLAN C] No tengo datos. Necesito tu ayuda humana.")
            nueva_preg_texto = input(f"Escribe una pregunta de Sí/No que sea VERDADERA para '{nuevo_obj}' pero FALSA para '{mejor_opcion}':\n> ")
            id_nueva_preg = f"preg_{len(preguntas) + 1}"
            preguntas[id_nueva_preg] = nueva_preg_texto
            objetos[nuevo_obj][id_nueva_preg] = 1.0

        # Nos aseguramos de separar ambos objetos matemáticamente
        # Si no se asignó en el Plan B, lo asignamos aquí asumiendo que el nuevo es 1.0 y el perdedor -1.0
        if id_nueva_preg not in objetos[nuevo_obj]:
            objetos[nuevo_obj][id_nueva_preg] = 1.0
        objetos[mejor_opcion][id_nueva_preg] = -1.0
        
        print("¡Conocimiento matricial expandido y asegurado! 🧠✨")
        guardar_conocimiento(datos)

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    print("--- MOTOR IA: RED NEURONAL PONDERADA (TIPO 20Q) ---")
    while True:
        jugar()
        if input("\n¿Quieres jugar otra vez? (s/n): ").lower().strip() != 's':
            print("Desconectando de la Matrix... ¡Hasta pronto!")
            break