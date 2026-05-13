import json
import os
import time
import google.generativeai as genai

ARCHIVO_CEREBRO = "cerebro.json"

# 🛑 AQUÍ PONDRÁS TU CLAVE DE API GRATUITA
API_KEY = "TU_CLAVE_API_AQUI" 
genai.configure(api_key=API_KEY)

# Usamos el modelo más rápido y económico
modelo = genai.GenerativeModel('gemini-1.5-flash')

def cargar_conocimiento():
    if os.path.exists(ARCHIVO_CEREBRO):
        with open(ARCHIVO_CEREBRO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"objetos": {}, "preguntas": {}}

def guardar_conocimiento(datos):
    with open(ARCHIVO_CEREBRO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def evaluar_con_ia(objeto, preguntas_dict):
    """Le pide a la IA que responda todas las preguntas para un objeto."""
    
    # Preparamos el formato de las preguntas para la IA
    texto_preguntas = "\n".join([f"- {id_preg}: {texto}" for id_preg, texto in preguntas_dict.items()])
    
    prompt = f"""
    Eres un experto etiquetador de datos lógicos.
    Analiza el objeto: "{objeto}".
    
    Responde a las siguientes preguntas sobre este objeto usando estrictamente:
    's' (para Sí), 'n' (para No), o 't' (para Tal vez / Depende / Irrelevante).
    
    Preguntas:
    {texto_preguntas}
    
    Devuelve ÚNICAMENTE un objeto JSON válido donde las claves sean los IDs de las preguntas y los valores sean tus respuestas ('s', 'n', 't'). No uses markdown, ni comillas invertidas, solo el texto JSON puro.
    Ejemplo de salida: {{"preg_1": "s", "preg_2": "n"}}
    """
    
    try:
        respuesta = modelo.generate_content(prompt)
        # Limpiamos la respuesta por si la IA incluyó formato markdown
        texto_json = respuesta.text.strip().replace("```json", "").replace("```", "")
        evaluacion = json.loads(texto_json)
        return evaluacion
    except Exception as e:
        print(f"⚠️ Error al consultar a la IA: {e}")
        return None

def iniciar_entrenamiento_autonomo(lista_palabras):
    print("🤖 Iniciando Super-Bot Autónomo con IA Generativa...")
    datos = cargar_conocimiento()
    objetos = datos["objetos"]
    preguntas = datos["preguntas"]
    
    if not preguntas:
        print("❌ Tu cerebro no tiene preguntas base. Añade algunas primero.")
        return

    for palabra in lista_palabras:
        palabra = palabra.lower().strip()
        nombre_obj = f"un/una {palabra}"

        if nombre_obj in objetos:
            print(f"⏩ '{palabra.upper()}' ya está asimilado. Saltando...")
            continue
            
        print(f"\n🧠 Evaluando autónomamente: '{palabra.upper()}'...")
        
        # ¡Magia! La IA evalúa todas las preguntas en 1 segundo
        respuestas_ia = evaluar_con_ia(palabra, preguntas)
        
        if respuestas_ia:
            objetos[nombre_obj] = {}
            
            # Traducimos las respuestas 's/n/t' de la IA a nuestros pesos matemáticos
            for id_preg, resp in respuestas_ia.items():
                if resp == 's':
                    objetos[nombre_obj][id_preg] = 1.0
                elif resp == 'n':
                    objetos[nombre_obj][id_preg] = -1.0
                # Si es 't', simplemente no lo agregamos (peso 0.0)
                    
            guardar_conocimiento(datos)
            print(f"✅ ¡Completado! Matriz densa generada para '{palabra.upper()}'.")
        else:
            print(f"❌ Falló la evaluación para '{palabra}'.")
            
        # Pausa para no saturar el límite gratuito de la API
        time.sleep(3)
        
    print("\n🎉 Entrenamiento Autónomo Finalizado.")

if __name__ == "__main__":
    paquete_entrenamiento = ["tigre", "televisor", "helado", "motocicleta"]
    iniciar_entrenamiento_autonomo(paquete_entrenamiento)