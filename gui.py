import customtkinter as ctk
import json
import os
import requests
import random

# Configuración del tema visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class IA20Preguntas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Oráculo IA - 20 Preguntas")
        self.geometry("700x450")
        self.resizable(False, False)
        
        # Carga de la Matrix
        self.archivo_cerebro = "cerebro.json"
        self.datos = self.cargar_datos()
        self.objetos = self.datos.get("objetos", {})
        self.preguntas = self.datos.get("preguntas", {})
        
        # Variables del motor
        self.puntajes = {}
        self.preguntas_hechas = 0
        self.limite = 20
        self.preguntas_pendientes = []
        self.mejor_opcion = ""
        
        self.construir_interfaz()
        self.reiniciar_juego()

    def cargar_datos(self):
        if os.path.exists(self.archivo_cerebro):
            with open(self.archivo_cerebro, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"objetos": {}, "preguntas": {}}

    def guardar_datos(self):
        with open(self.archivo_cerebro, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)

    def construir_interfaz(self):
        # Etiqueta superior (Contador)
        self.lbl_estado = ctk.CTkLabel(self, text="Inicializando...", font=("Roboto", 14), text_color="gray")
        self.lbl_estado.pack(pady=(30, 5))
        
        # Etiqueta principal (Pregunta)
        self.lbl_pregunta = ctk.CTkLabel(self, text="", font=("Roboto", 26, "bold"), wraplength=600)
        self.lbl_pregunta.pack(pady=(20, 40), expand=True)
        
        # Zona de botones: Fase de Juego
        self.frame_juego = ctk.CTkFrame(self, fg_color="transparent")
        
        self.btn_si = ctk.CTkButton(self.frame_juego, text="SÍ", width=130, height=45, font=("Roboto", 16, "bold"), fg_color="#28C76F", hover_color="#22a85e", command=lambda: self.responder('s'))
        self.btn_si.pack(side="left", padx=15)
        
        self.btn_talvez = ctk.CTkButton(self.frame_juego, text="TAL VEZ", width=130, height=45, font=("Roboto", 16, "bold"), fg_color="#555555", hover_color="#444444", command=lambda: self.responder('t'))
        self.btn_talvez.pack(side="left", padx=15)
        
        self.btn_no = ctk.CTkButton(self.frame_juego, text="NO", width=130, height=45, font=("Roboto", 16, "bold"), fg_color="#EA5455", hover_color="#ce4a4a", command=lambda: self.responder('n'))
        self.btn_no.pack(side="left", padx=15)
        
        # Zona de botones: Fase de Adivinación
        self.frame_adivinar = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_correcto = ctk.CTkButton(self.frame_adivinar, text="¡SÍ, ACERTASTE!", width=200, height=45, font=("Roboto", 16, "bold"), fg_color="#28C76F", hover_color="#22a85e", command=self.victoria_ia)
        self.btn_correcto.pack(side="left", padx=15)
        self.btn_incorrecto = ctk.CTkButton(self.frame_adivinar, text="NO, TE EQUIVOCASTE", width=200, height=45, font=("Roboto", 16, "bold"), fg_color="#EA5455", hover_color="#ce4a4a", command=self.derrota_ia)
        self.btn_incorrecto.pack(side="left", padx=15)

        # Botón de Reinicio
        self.btn_reiniciar = ctk.CTkButton(self, text="JUGAR DE NUEVO", width=200, height=45, font=("Roboto", 16, "bold"), command=self.reiniciar_juego)

    def reiniciar_juego(self):
        if not self.objetos or not self.preguntas:
            self.lbl_pregunta.configure(text="El cerebro.json no está listo.")
            return
            
        self.puntajes = {nombre: 0.0 for nombre in self.objetos.keys()}
        self.preguntas_pendientes = list(self.preguntas.items())
        random.shuffle(self.preguntas_pendientes)
        self.preguntas_hechas = 0
        
        self.btn_reiniciar.pack_forget()
        self.frame_adivinar.pack_forget()
        self.frame_juego.pack(pady=20)
        
        self.mostrar_siguiente_pregunta()

    def mostrar_siguiente_pregunta(self):
        # Sensor de finalización
        if self.preguntas_hechas >= self.limite or not self.preguntas_pendientes:
            self.hacer_adivinanza()
            return
            
        self.pregunta_actual_id, self.pregunta_actual_texto = self.preguntas_pendientes.pop(0)
        self.lbl_estado.configure(text=f"Pregunta {self.preguntas_hechas + 1} de {self.limite}")
        self.lbl_pregunta.configure(text=self.pregunta_actual_texto)

    def responder(self, resp):
        self.preguntas_hechas += 1
        
        # Ajuste de matriz de pesos
        for obj_nombre, atributos in self.objetos.items():
            peso = atributos.get(self.pregunta_actual_id, 0.0)
            if resp == 's': self.puntajes[obj_nombre] += peso
            elif resp == 'n': self.puntajes[obj_nombre] -= peso
            
        # Umbral de confianza (Early Stopping)
        ranking = sorted(self.puntajes.items(), key=lambda x: x[1], reverse=True)
        if len(ranking) >= 2:
            if (ranking[0][1] - ranking[1][1]) >= 2.0:
                self.hacer_adivinanza()
                return
                
        self.mostrar_siguiente_pregunta()

    def hacer_adivinanza(self):
        ranking = sorted(self.puntajes.items(), key=lambda x: x[1], reverse=True)
        self.mejor_opcion = ranking[0][0]
        
        self.lbl_estado.configure(text="¡Análisis completado!")
        self.lbl_pregunta.configure(text=f"¿Estás pensando en\n{self.mejor_opcion.upper()}?")
        
        self.frame_juego.pack_forget()
        self.frame_adivinar.pack(pady=20)

    def victoria_ia(self):
        self.lbl_estado.configure(text="Fin del juego")
        self.lbl_pregunta.configure(text="¡La probabilidad matemática nunca falla! 🤖🏆")
        self.frame_adivinar.pack_forget()
        self.btn_reiniciar.pack(pady=20)

    def derrota_ia(self):
        self.frame_adivinar.pack_forget()
        self.lbl_estado.configure(text="Aprendiendo de la Matrix...")
        self.lbl_pregunta.configure(text="¡Vaya! La entropía me ha superado.\nPermíteme investigar...")
        self.update() 
        
        dialogo = ctk.CTkInputDialog(text="¿En qué estabas pensando? (ej: guitarra, barco):", title="Auto-Entrenamiento")
        nuevo_obj = dialogo.get_input()
        
        if nuevo_obj:
            self.aprender_nuevo_objeto(nuevo_obj.lower().strip())
        else:
            self.btn_reiniciar.pack(pady=20)

    def aprender_nuevo_objeto(self, nuevo_obj):
        if nuevo_obj not in self.objetos:
            self.objetos[nuevo_obj] = {}
            
        # PLAN A: Conexión a Wikidata
        pregunta_api = self.consultar_wikidata(nuevo_obj)
        
        if pregunta_api:
            id_nueva = f"preg_{len(self.preguntas) + 1}"
            self.preguntas[id_nueva] = pregunta_api
            self.objetos[nuevo_obj][id_nueva] = 1.0
            self.objetos[self.mejor_opcion][id_nueva] = -1.0
            self.guardar_datos()
            
            self.lbl_estado.configure(text="Red Neuronal Actualizada")
            self.lbl_pregunta.configure(text=f"¡Wikidata me ha enseñado algo nuevo!\nHe agregado la regla: {pregunta_api}")
        else:
            # PLAN C: Intervención Manual
            dialogo = ctk.CTkInputDialog(text=f"Escribe una pregunta de Sí/No que sea VERDADERA para '{nuevo_obj}' pero FALSA para '{self.mejor_opcion}':", title="Modo Manual")
            pregunta_manual = dialogo.get_input()
            
            if pregunta_manual:
                id_nueva = f"preg_{len(self.preguntas) + 1}"
                self.preguntas[id_nueva] = pregunta_manual
                self.objetos[nuevo_obj][id_nueva] = 1.0
                self.objetos[self.mejor_opcion][id_nueva] = -1.0
                self.guardar_datos()
                
                self.lbl_estado.configure(text="Red Neuronal Actualizada")
                self.lbl_pregunta.configure(text="¡Conocimiento matricial expandido gracias a ti! 🧠✨")
        
        self.btn_reiniciar.pack(pady=20)

    def consultar_wikidata(self, palabra):
        palabra_limpia = palabra.replace("un ", "").replace("una ", "").replace("el ", "").replace("la ", "")
        url = "https://www.wikidata.org/w/api.php"
        parametros = {"action": "wbsearchentities", "search": palabra_limpia, "language": "es", "uselang": "es", "strictlanguage": "1", "format": "json"}
        cabeceras = {"User-Agent": "GUI_Portafolio_Game/1.0"}
        
        try:
            r = requests.get(url, params=parametros, headers=cabeceras, timeout=4)
            if r.status_code == 200:
                resultados = r.json().get('search', [])
                if resultados:
                    desc = resultados[0].get('description')
                    if desc and "Wikimedia" not in desc and "Wikipedia" not in desc:
                        return f"¿Es un/una {desc}?"
        except:
            pass
        return None

if __name__ == "__main__":
    app = IA20Preguntas()
    app.mainloop()