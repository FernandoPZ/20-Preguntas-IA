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
# CONEXIÓN A LA MATRIX (WIKIDATA - MODO DEBUG)
# ==========================================
def consultar_wikidata(palabra):
    """Busca atributos de una palabra en Internet usando la API de Wikidata."""
    palabra_limpia = palabra.replace("un ", "").replace("una ", "").replace("el ", "").replace("la ", "")
    print(f"\n🌐 [DEBUG] Iniciando búsqueda para: '{palabra_limpia}'")
    
    url = "https://www.wikidata.org/w/api.php"
    parametros = {
        "action": "wbsearchentities",
        "search": palabra_limpia,
        "language": "es",
        "uselang": "es",
        "strictlanguage": "1",
        "format": "json"
    }
    
    # TARJETA DE IDENTIFICACIÓN
    cabeceras = {
        "User-Agent": "MotorIA_Portafolio/1.0 (aprendiendo_python@developer.com)"
    }
    
    try:
        respuesta = requests.get(url, params=parametros, headers=cabeceras, timeout=5)
        
        print(f"🔗 [DEBUG] URL generada: {respuesta.url}")
        print(f"📡 [DEBUG] Estado HTTP: {respuesta.status_code}")
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultados = datos.get('search', [])
            
            if not resultados:
                print("❌ [DEBUG] Wikidata devolvió una lista vacía. No existe la palabra.")
                return None
                
            print(f"✅ [DEBUG] Se encontraron {len(resultados)} posibles coincidencias.")
            
            primer_resultado = resultados[0]
            descripcion = primer_resultado.get('description')
            
            print(f"📄 [DEBUG] Descripción extraída: '{descripcion}'")
            
            if descripcion:
                if "Wikimedia" in descripcion or "Wikipedia" in descripcion:
                    print("❌ [DEBUG] Es una página de desambiguación. No sirve para jugar.")
                else:
                    print("✨ [DEBUG] ¡Descripción válida encontrada!")
                    return f"¿Es un/una {descripcion}?"
            else:
                print("❌ [DEBUG] El objeto existe, pero no tiene una descripción redactada.")
                
            return None
        else:
            print(f"❌ [DEBUG] Error del servidor de Wikidata: {respuesta.text}")
            return None
            
    except requests.RequestException as e:
        print(f"⚠️ [DEBUG] Error crítico de red: {e}")
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
        pregunta_internet = consultar_wikidata(nuevo_obj)
        if pregunta_internet:
            print(f"💡 [PLAN A] Wikidata sugiere: '{pregunta_internet}'")
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