
import customtkinter as ctk
import serial
import csv
import os

from datetime import datetime
from tkinter import messagebox
from interfaz import InterfazEncuesta


PUERTO = "COM3"  #Sahonero cambiá si es necesario el puerto!
VELOCIDAD = 9600

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(CARPETA, "respuestas.csv")


class ControlEncuesta:

    def __init__(self, ventana, conexion):

        self.ventana = ventana
        self.conexion = conexion

        self.estado = "standby"
        self.buffer = ""

        self.interfaz = InterfazEncuesta(
            ventana,
            self.registrar_respuesta
        )

        self.ventana.after(2000, self.leer_arduino)

    def leer_arduino(self):

        try:

            if self.conexion.in_waiting > 0:

                datos = self.conexion.read(
                    self.conexion.in_waiting
                ).decode("utf-8", errors="ignore")

                self.buffer += datos

                while "\n" in self.buffer:

                    mensaje, self.buffer = self.buffer.split(
                        "\n", 1
                    )

                    if mensaje.strip() == "INICIO":
                        self.iniciar_encuesta()

        except serial.SerialException:

            messagebox.showerror(
                "Error",
                "Se perdio la conexion con Arduino."
            )
            return

        self.ventana.after(100, self.leer_arduino)

    def iniciar_encuesta(self):

        if self.estado == "standby":

            self.estado = "encuesta"

            self.interfaz.mostrar_encuesta()

    def registrar_respuesta(self, calificacion):

        if self.estado != "encuesta":
            return

        try:

            existe = (
                os.path.exists(ARCHIVO_CSV)
                and os.path.getsize(ARCHIVO_CSV) > 0
            )

            with open(
                ARCHIVO_CSV,
                "a",
                newline="",
                encoding="utf-8"
            ) as archivo:

                escritor = csv.writer(archivo)

                if not existe:
                    escritor.writerow([
                        "Fecha y hora",
                        "Calificacion"
                    ])

                escritor.writerow([
                    datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    calificacion
                ])

        except OSError:

            messagebox.showerror(
                "Error",
                "No se pudo guardar la respuesta."
            )
            return

        try:

            self.conexion.write(b"FIN\n")
            self.conexion.flush()

        except serial.SerialException:

            messagebox.showerror(
                "Error",
                "No se pudo enviar la orden a Arduino."
            )
            return

        self.estado = "gracias"

        self.interfaz.mostrar_agradecimiento()

        self.ventana.after(
            2500,
            self.volver_standby
        )

    def volver_standby(self):

        self.estado = "standby"

        self.interfaz.mostrar_standby()


def main():

    ctk.set_appearance_mode("light")

    ventana = ctk.CTk()
    ventana.withdraw()

    try:

        conexion = serial.Serial(
            PUERTO,
            VELOCIDAD,
            timeout=0
        )

    except serial.SerialException:

        messagebox.showerror(
            "Error de conexion",
            "No se pudo conectar con Arduino.\n"
            "Revisa el puerto COM y el cable USB."
        )

        ventana.destroy()
        return

    ventana.deiconify()

    ControlEncuesta(ventana, conexion)

    def cerrar_programa():

        if conexion.is_open:
            conexion.close()

        ventana.destroy()

    ventana.protocol(
        "WM_DELETE_WINDOW",
        cerrar_programa
    )

    ventana.mainloop()


if __name__ == "__main__":
    main()
