import json
import time
import requests
import os

ARCHIVO_CEREBRO = "cerebro.json"

def cargar_conocimiento():
    if os.path.exists(ARCHIVO_CEREBRO):
        with open(ARCHIVO_CEREBRO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"objetos": {}, "preguntas": {}}

def guardar_conocimiento(datos):
    with open(ARCHIVO_CEREBRO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def consultar_wikidata(palabra):
    palabra_limpia = palabra.replace("un ", "").replace("una ", "").replace(" ", "_")
    url = "https://www.wikidata.org/w/api.php"
    parametros = {"action": "wbsearchentities", "search": palabra_limpia, "language": "es", "uselang": "es", "strictlanguage": "1", "format": "json"}
    cabeceras = {"User-Agent": "BotEntrenador_Portafolio/2.0"}
    
    try:
        respuesta = requests.get(url, params=parametros, headers=cabeceras, timeout=5)
        if respuesta.status_code == 200:
            resultados = respuesta.json().get('search', [])
            if resultados:
                desc = resultados[0].get('description')
                if desc and "Wikimedia" not in desc and "Wikipedia" not in desc:
                    return f"¿Es un/una {desc}?"
    except:
        pass
    return None

def iniciar_entrenamiento_avanzado(lista_palabras):
    print("🤖 Iniciando Bot de Entrenamiento (Modo Human-in-the-Loop)...")
    datos = cargar_conocimiento()
    objetos = datos["objetos"]
    preguntas = datos["preguntas"]

    for palabra in lista_palabras:
        palabra = palabra.lower().strip()
        nombre_obj = f"un/una {palabra}"

        if nombre_obj in objetos:
            print(f"\n⏩ '{palabra.upper()}' ya existe en la matriz. Saltando...")
            continue

        print(f"\n========================================")
        print(f"🔍 BOT: Investigando '{palabra.upper()}' en Wikidata...")
        nueva_pregunta = consultar_wikidata(palabra)

        if nueva_pregunta:
            # 1. El bot aporta la pregunta única de Internet
            id_nueva = f"preg_{len(preguntas) + 1}"
            preguntas[id_nueva] = nueva_pregunta
            objetos[nombre_obj] = {id_nueva: 1.0}
            print(f"✅ BOT: Aprendí la regla -> {nueva_pregunta}")
            
            # 2. Tú aportas el contexto (Revaloración de preguntas existentes)
            print(f"\n🧠 HUMANO: Ayúdame a integrar '{palabra.upper()}' a la red neuronal:")
            print("   (Responde s/n/t)")
            
            # Extraemos una copia de las preguntas para no modificar el diccionario mientras iteramos
            preguntas_existentes = list(preguntas.items())
            
            for id_preg, texto_preg in preguntas_existentes:
                if id_preg == id_nueva: 
                    continue # Saltamos la que el bot acaba de agregar
                    
                resp = input(f"   -> {texto_preg} : ").lower().strip()
                if resp == 's':
                    objetos[nombre_obj][id_preg] = 1.0
                elif resp == 'n':
                    objetos[nombre_obj][id_preg] = -1.0
                # Si es 't', no guardamos nada, se queda como 0.0 implícito

            guardar_conocimiento(datos)
            print(f"💾 '{palabra.upper()}' asimilado y guardado en la Matriz Densa.")
        else:
            print(f"❌ BOT: La Matrix no tiene datos útiles para '{palabra}'.")

        # Respetamos el servidor
        time.sleep(1.5) 

    print("\n🎉 Entrenamiento masivo finalizado.")

if __name__ == "__main__":
    # ¡Aquí tienes un paquete de entrenamiento intensivo!
    paquete_entrenamiento = [
        "leon", "computadora", "helicoptero", "hamburguesa",
        "serpiente", "reloj", "motocicleta", "submarino"
    ]
    iniciar_entrenamiento_avanzado(paquete_entrenamiento)