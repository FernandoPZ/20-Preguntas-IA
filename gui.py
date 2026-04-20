import customtkinter as ctk
import motor_ia

# Configuración visual base
ctk.set_appearance_mode("Dark")

class OraculoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Oráculo IA - 20 Preguntas")
        self.geometry("600x450")
        self.minsize(500, 400)
        
        # 1. Cargamos el cerebro arbol.py
        self.cerebro_raiz = motor_ia.cargar_conocimiento()
        self.nodo_actual = self.cerebro_raiz
        
        # Variables temporales para cuando la IA aprende
        self.nuevo_elemento = ""
        self.nueva_pregunta = ""
        self.fase = "navegar" # Fases: navegar, adivinar, aprender_elemento, aprender_pregunta, aprender_respuesta, fin
        
        self.construir_ui()
        self.actualizar_pantalla()

    def construir_ui(self):
        # --- Encabezado ---
        self.lbl_titulo = ctk.CTkLabel(self, text="🧠 Lector de Mentes IA", font=("Arial", 28, "bold"))
        self.lbl_titulo.pack(pady=(30, 10))
        
        # --- Pantalla Principal (El "rostro" de la IA) ---
        self.frame_pantalla = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        self.frame_pantalla.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.lbl_mensaje = ctk.CTkLabel(self.frame_pantalla, text="", font=("Arial", 20), wraplength=450)
        self.lbl_mensaje.pack(expand=True, pady=20)
        
        # --- Controles (Botones Sí/No) ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_si = ctk.CTkButton(self.frame_botones, text="SÍ", command=lambda: self.procesar_respuesta("s"), 
                                    fg_color="#28C76F", hover_color="#21A05A", font=("Arial", 16, "bold"), width=120, height=40)
        self.btn_si.pack(side="left", padx=20)
        
        self.btn_no = ctk.CTkButton(self.frame_botones, text="NO", command=lambda: self.procesar_respuesta("n"), 
                                    fg_color="#FF4C4C", hover_color="#CC3D3D", font=("Arial", 16, "bold"), width=120, height=40)
        self.btn_no.pack(side="right", padx=20)
        
        # --- Controles (Entrada de Texto para Aprender) ---
        self.frame_input = ctk.CTkFrame(self, fg_color="transparent")
        self.entrada_texto = ctk.CTkEntry(self.frame_input, width=300, height=40, font=("Arial", 16))
        self.entrada_texto.pack(side="left", padx=(0, 10))
        # Vinculamos la tecla 'Enter' para mayor comodidad
        self.entrada_texto.bind("<Return>", lambda e: self.procesar_texto())
        
        self.btn_enviar = ctk.CTkButton(self.frame_input, text="Enviar", command=self.procesar_texto, height=40)
        self.btn_enviar.pack(side="left")
        
        # --- Botón de Reinicio ---
        self.btn_reiniciar = ctk.CTkButton(self, text="Jugar de Nuevo", command=self.reiniciar_juego, height=40)

    # LÓGICA DE LA MÁQUINA DE ESTADOS
    def actualizar_pantalla(self):
        """Muestra u oculta controles dependiendo de la fase en la que estemos."""
        self.frame_botones.pack_forget()
        self.frame_input.pack_forget()
        self.btn_reiniciar.pack_forget()
        self.entrada_texto.delete(0, 'end')

        if self.fase == "navegar":
            self.lbl_mensaje.configure(text=self.nodo_actual.texto)
            self.frame_botones.pack(pady=(0, 30))
            
        elif self.fase == "adivinar":
            self.lbl_mensaje.configure(text=f"¿Estás pensando en {self.nodo_actual.texto}?")
            self.frame_botones.pack(pady=(0, 30))
            
        elif self.fase == "aprender_elemento":
            self.lbl_mensaje.configure(text="¡Me ganaste! ¿En qué estabas pensando?\n(Ejemplo: un gato)")
            self.frame_input.pack(pady=(0, 30))
            self.entrada_texto.focus()
            
        elif self.fase == "aprender_pregunta":
            self.lbl_mensaje.configure(text=f"Escribe una pregunta para distinguir:\n'{self.nuevo_elemento}' de '{self.nodo_actual.texto}'")
            self.frame_input.pack(pady=(0, 30))
            self.entrada_texto.focus()
            
        elif self.fase == "aprender_respuesta":
            self.lbl_mensaje.configure(text=f"Para '{self.nuevo_elemento}',\n¿la respuesta a tu pregunta es SÍ o NO?")
            self.frame_botones.pack(pady=(0, 30))
            
        elif self.fase == "fin":
            self.btn_reiniciar.pack(pady=(0, 30))

    def procesar_respuesta(self, respuesta):
        if self.fase == "navegar":
            self.nodo_actual = self.nodo_actual.nodo_si if respuesta == "s" else self.nodo_actual.nodo_no
            if self.nodo_actual.es_hoja:
                self.fase = "adivinar"
            self.actualizar_pantalla()
            
        elif self.fase == "adivinar":
            if respuesta == "s":
                self.lbl_mensaje.configure(text="¡Jaja! ¡La Inteligencia Artificial gana de nuevo! 🤖🏆")
                self.fase = "fin"
            else:
                self.fase = "aprender_elemento"
            self.actualizar_pantalla()
            
        elif self.fase == "aprender_respuesta":
            # 1. Transformamos la hoja en una nueva pregunta
            viejo_texto = self.nodo_actual.texto
            self.nodo_actual.texto = self.nueva_pregunta
            self.nodo_actual.es_hoja = False
            
            # 2. Conectamos las hojas nuevas
            if respuesta == 's':
                self.nodo_actual.nodo_si = motor_ia.Nodo(self.nuevo_elemento, es_hoja=True)
                self.nodo_actual.nodo_no = motor_ia.Nodo(viejo_texto, es_hoja=True)
            else:
                self.nodo_actual.nodo_no = motor_ia.Nodo(self.nuevo_elemento, es_hoja=True)
                self.nodo_actual.nodo_si = motor_ia.Nodo(viejo_texto, es_hoja=True)
                
            # 3. Usamos la función de arbol.py para guardar
            motor_ia.guardar_conocimiento(self.cerebro_raiz)
            self.lbl_mensaje.configure(text="¡Gracias! He expandido mi conocimiento. 🧠✨\n(Memoria guardada en el disco)")
            self.fase = "fin"
            self.actualizar_pantalla()

    def procesar_texto(self):
        texto = self.entrada_texto.get().strip().lower()
        if not texto: return
        
        if self.fase == "aprender_elemento":
            self.nuevo_elemento = texto
            self.fase = "aprender_pregunta"
            self.actualizar_pantalla()
            
        elif self.fase == "aprender_pregunta":
            # Autocorrección estética rápida
            if not texto.startswith("¿"): texto = "¿" + texto
            if not texto.endswith("?"): texto = texto + "?"
            self.nueva_pregunta = texto
            self.fase = "aprender_respuesta"
            self.actualizar_pantalla()

    def reiniciar_juego(self):
        self.nodo_actual = self.cerebro_raiz
        self.fase = "navegar"
        self.actualizar_pantalla()

if __name__ == "__main__":
    app = OraculoApp()
    app.mainloop()