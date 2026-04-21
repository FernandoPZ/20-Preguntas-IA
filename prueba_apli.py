import requests

def extraer_conocimiento(palabra):
    print(f"Consultando la red neuronal global para: '{palabra}'...\n")
    
    # La URL oficial de la API de ConceptNet (buscando en español 'es')
    url = f"https://api.conceptnet.io/c/es/{palabra}?limit=15"
    
    # Hacemos la petición a Internet
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        
        # Filtramos y traducimos las relaciones para entenderlas
        relaciones_traducidas = {
            "IsA": "Es un/una",
            "CapableOf": "Es capaz de",
            "HasA": "Tiene",
            "UsedFor": "Se usa para",
            "AtLocation": "Se encuentra en"
        }
        
        print(f"--- RESULTADOS PARA: {palabra.upper()} ---")
        for edge in datos.get('edges', []):
            relacion_ingles = edge['rel']['label']
            destino = edge['end']['label']
            
            # Solo mostramos las relaciones que nos sirven para el juego
            if relacion_ingles in relaciones_traducidas:
                relacion_esp = relaciones_traducidas[relacion_ingles]
                print(f"- {relacion_esp} -> {destino}")
    else:
        print("Error al conectar con la Matrix.")

# --- PRUEBA ---
if __name__ == "__main__":
    extraer_conocimiento("automovil")