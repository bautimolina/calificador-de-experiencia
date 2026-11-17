
import customtkinter as ctk


class InterfazEncuesta:

    def __init__(self, ventana, al_calificar):

        self.ventana = ventana
        self.al_calificar = al_calificar

        self.fondo = "#F4F0E8"
        self.texto = "#38342F"
        self.dorado = "#C69B50"
        self.dorado_hover = "#AA803B"
        self.secundario = "#77716A"

        self.ventana.title("Encuesta de atencion")
        self.ventana.geometry("750x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(fg_color=self.fondo)

        self.crear_standby()
        self.crear_encuesta()
        self.crear_agradecimiento()

        self.mostrar_standby()

    def crear_standby(self):

        self.frame_standby = ctk.CTkFrame(
            self.ventana,
            fg_color=self.fondo,
            corner_radius=0
        )

        self.frame_standby.place(
            relwidth=1,
            relheight=1
        )

        ctk.CTkLabel(
            self.frame_standby,
            text="ENCUESTA DE ATENCION",
            font=("Arial", 30, "bold"),
            text_color=self.texto
        ).pack(pady=(105, 25))

        ctk.CTkLabel(
            self.frame_standby,
            text="¡Tu opinion nos importa!",
            font=("Arial", 24, "bold"),
            text_color=self.texto
        ).pack(pady=10)

        ctk.CTkLabel(
            self.frame_standby,
            text="Conecte el cable para comenzar",
            font=("Arial", 17),
            text_color=self.secundario
        ).pack(pady=10)

        ctk.CTkLabel(
            self.frame_standby,
            text="Esperando una nueva encuesta...",
            font=("Arial", 14),
            text_color=self.dorado
        ).pack(pady=35)

    def crear_encuesta(self):

        self.frame_encuesta = ctk.CTkFrame(
            self.ventana,
            fg_color=self.fondo,
            corner_radius=0
        )

        self.frame_encuesta.place(
            relwidth=1,
            relheight=1
        )

        ctk.CTkLabel(
            self.frame_encuesta,
            text="¿COMO CALIFICARIAS NUESTRA ATENCION?",
            font=("Arial", 24, "bold"),
            text_color=self.texto
        ).pack(pady=(105, 20))

        ctk.CTkLabel(
            self.frame_encuesta,
            text="Selecciona una calificacion del 1 al 5",
            font=("Arial", 17),
            text_color=self.secundario
        ).pack(pady=10)

        fila_estrellas = ctk.CTkFrame(
            self.frame_encuesta,
            fg_color="transparent"
        )

        fila_estrellas.pack(pady=30)

        for numero in range(1, 6):

            boton = ctk.CTkButton(
                fila_estrellas,
                text=f"★\n{numero}",
                width=85,
                height=85,
                font=("Arial", 24, "bold"),
                fg_color=self.dorado,
                hover_color=self.dorado_hover,
                text_color="#FFFFFF",
                corner_radius=12,
                command=lambda n=numero: self.al_calificar(n)
            )

            boton.grid(
                row=0,
                column=numero - 1,
                padx=7
            )

        ctk.CTkLabel(
            self.frame_encuesta,
            text="1 = Muy mala                 5 = Excelente",
            font=("Arial", 14),
            text_color=self.secundario
        ).pack(pady=15)

    def crear_agradecimiento(self):

        self.frame_gracias = ctk.CTkFrame(
            self.ventana,
            fg_color=self.fondo,
            corner_radius=0
        )

        self.frame_gracias.place(
            relwidth=1,
            relheight=1
        )

        ctk.CTkLabel(
            self.frame_gracias,
            text="¡MUCHAS GRACIAS!",
            font=("Arial", 32, "bold"),
            text_color=self.dorado
        ).pack(pady=(155, 25))

        ctk.CTkLabel(
            self.frame_gracias,
            text="Tu opinion nos ayuda a mejorar.",
            font=("Arial", 20),
            text_color=self.texto
        ).pack(pady=10)

        ctk.CTkLabel(
            self.frame_gracias,
            text="¡Esperamos volver a verte!",
            font=("Arial", 16),
            text_color=self.secundario
        ).pack(pady=10)

    def mostrar_standby(self):

        self.frame_standby.tkraise()

    def mostrar_encuesta(self):

        self.frame_encuesta.tkraise()

    def mostrar_agradecimiento(self):

        self.frame_gracias.tkraise()