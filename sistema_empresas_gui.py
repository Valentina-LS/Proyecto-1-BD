"""Interfaz grafica tkinter para CRUD de empresas."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

from sistema_empresas import Empresa, GestorEmpresas


class SistemaEmpresasGUI:
    """Controla la interfaz grafica y conecta acciones con el gestor CRUD."""

    def __init__(self, root: tk.Tk) -> None:
        """Inicializa ventana, estado y widgets principales."""
        self.root = root
        self.root.title("Sistema de Empresas - GUI")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        self.gestor = GestorEmpresas()

        self.var_nit = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_presupuesto = tk.StringVar()

        self._construir_interfaz()

    def _construir_interfaz(self) -> None:
        """Crea layout, campos, botones y area de salida."""
        titulo = tk.Label(
            self.root,
            text="Sistema de Empresas (Enfoque Educativo)",
            bg="white",
            fg="black",
            font=("Segoe UI", 14, "bold"),
        )
        titulo.pack(pady=10)

        frame_form = tk.Frame(self.root, bg="white")
        frame_form.pack(fill="x", padx=20, pady=10)

        self._crear_campo(frame_form, "NIT", self.var_nit, 0)
        self._crear_campo(frame_form, "Nombre empresa", self.var_nombre, 1)
        self._crear_campo(frame_form, "Direccion", self.var_direccion, 2)
        self._crear_campo(frame_form, "Presupuesto anual", self.var_presupuesto, 3)

        frame_botones = tk.Frame(self.root, bg="white")
        frame_botones.pack(fill="x", padx=20, pady=10)

        botones = [
            ("Adicionar", self.adicionar),
            ("Consultar", self.consultar),
            ("Actualizar", self.actualizar),
            ("Eliminar", self.eliminar),
            ("Listar todas", self.listar),
            ("Importar CSV", self.importar_csv),
            ("Exportar CSV", self.exportar_csv),
            ("Limpiar", self.limpiar_campos),
        ]

        for i, (texto, accion) in enumerate(botones):
            btn = tk.Button(
                frame_botones,
                text=texto,
                command=accion,
                bg="white",
                fg="black",
                activebackground="white",
                activeforeground="black",
                relief="solid",
                bd=1,
                padx=10,
                pady=5,
            )
            btn.grid(row=0, column=i, padx=4, pady=4)

        frame_salida = tk.Frame(self.root, bg="white")
        frame_salida.pack(fill="both", expand=True, padx=20, pady=10)

        lbl_salida = tk.Label(
            frame_salida,
            text="Salida",
            bg="white",
            fg="black",
            font=("Segoe UI", 11, "bold"),
        )
        lbl_salida.pack(anchor="w")

        self.txt_salida = tk.Text(
            frame_salida,
            bg="white",
            fg="black",
            insertbackground="black",
            relief="solid",
            bd=1,
            wrap="word",
        )
        self.txt_salida.pack(fill="both", expand=True, pady=5)

    def _crear_campo(self, contenedor: tk.Frame, etiqueta: str, variable: tk.StringVar, fila: int) -> None:
        """Crea una fila de etiqueta + entrada para el formulario."""
        lbl = tk.Label(contenedor, text=etiqueta + ":", bg="white", fg="black", anchor="w")
        lbl.grid(row=fila, column=0, sticky="w", padx=5, pady=4)

        ent = tk.Entry(
            contenedor,
            textvariable=variable,
            bg="white",
            fg="black",
            insertbackground="black",
            relief="solid",
            bd=1,
            width=60,
        )
        ent.grid(row=fila, column=1, sticky="w", padx=5, pady=4)

    def _leer_formulario(self) -> tuple[str, str, str, float] | None:
        """Lee y valida campos del formulario."""
        nit = self.var_nit.get().strip()
        nombre = self.var_nombre.get().strip()
        direccion = self.var_direccion.get().strip()
        presupuesto_txt = self.var_presupuesto.get().strip()

        if not nit:
            messagebox.showerror("Error", "El NIT es obligatorio.")
            return None

        try:
            presupuesto = float(presupuesto_txt)
        except ValueError:
            messagebox.showerror("Error", "El presupuesto debe ser numerico.")
            return None

        return nit, nombre, direccion, presupuesto

    def _mostrar(self, texto: str) -> None:
        """Reemplaza el contenido del area de salida."""
        self.txt_salida.delete("1.0", tk.END)
        self.txt_salida.insert(tk.END, texto)

    def adicionar(self) -> None:
        """Agrega una empresa nueva desde el formulario."""
        datos = self._leer_formulario()
        if not datos:
            return

        nit, nombre, direccion, presupuesto = datos
        empresa = Empresa(nit, nombre, direccion, presupuesto)

        if self.gestor.adicionar(empresa):
            self._mostrar("Registro adicionado correctamente.")
        else:
            self._mostrar("No se pudo adicionar: ya existe una empresa con ese NIT.")

    def consultar(self) -> None:
        """Consulta una empresa por NIT y la muestra en pantalla."""
        nit = self.var_nit.get().strip()
        if not nit:
            messagebox.showerror("Error", "Ingrese el NIT para consultar.")
            return

        empresa = self.gestor.consultar(nit)
        if not empresa:
            self._mostrar("No se encontro una empresa con ese NIT.")
            return

        texto = (
            f"NIT: {empresa.nit}\n"
            f"Nombre empresa: {empresa.nombre_empresa}\n"
            f"Direccion: {empresa.direccion}\n"
            f"Presupuesto anual: {empresa.presupuesto_anual}"
        )
        self._mostrar(texto)

    def actualizar(self) -> None:
        """Actualiza una empresa existente por NIT."""
        datos = self._leer_formulario()
        if not datos:
            return

        nit, nombre, direccion, presupuesto = datos
        if self.gestor.actualizar(nit, nombre, direccion, presupuesto):
            self._mostrar("Registro actualizado correctamente.")
        else:
            self._mostrar("No se encontro una empresa con ese NIT.")

    def eliminar(self) -> None:
        """Elimina una empresa por NIT."""
        nit = self.var_nit.get().strip()
        if not nit:
            messagebox.showerror("Error", "Ingrese el NIT para eliminar.")
            return

        if self.gestor.eliminar(nit):
            self._mostrar("Registro eliminado correctamente.")
        else:
            self._mostrar("No se encontro una empresa con ese NIT.")

    def listar(self) -> None:
        """Lista todas las empresas registradas."""
        empresas = self.gestor.listar()
        if not empresas:
            self._mostrar("No hay empresas registradas.")
            return

        lineas = []
        for i, e in enumerate(empresas, start=1):
            lineas.append(
                f"Empresa #{i}\n"
                f"NIT: {e.nit}\n"
                f"Nombre empresa: {e.nombre_empresa}\n"
                f"Direccion: {e.direccion}\n"
                f"Presupuesto anual: {e.presupuesto_anual}\n"
            )

        self._mostrar("\n".join(lineas))

    def importar_csv(self) -> None:
        """Importa empresas desde archivo CSV con delimitador '|'."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo para importar",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return

        try:
            insertados, omitidos = self.gestor.importar_csv(ruta)
            self._mostrar(
                f"Importacion finalizada. Insertados: {insertados}. Omitidos: {omitidos}."
            )
        except OSError as exc:
            messagebox.showerror("Error", f"No se pudo importar el archivo: {exc}")

    def exportar_csv(self) -> None:
        """Exporta las empresas actuales a un archivo CSV."""
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo de exportacion",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return

        try:
            self.gestor.exportar_csv(ruta)
            self._mostrar("Exportacion finalizada correctamente.")
        except OSError as exc:
            messagebox.showerror("Error", f"No se pudo exportar el archivo: {exc}")

    def limpiar_campos(self) -> None:
        """Limpia los campos del formulario y la salida."""
        self.var_nit.set("")
        self.var_nombre.set("")
        self.var_direccion.set("")
        self.var_presupuesto.set("")
        self._mostrar("Campos limpiados.")


def main() -> None:
    """Punto de entrada de la aplicacion grafica."""
    root = tk.Tk()
    app = SistemaEmpresasGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
