"""
Programa educativo de Base de Datos (simulacion CRUD de empresas).

Objetivo:
- Practicar operaciones basicas tipo base de datos sin instalar dependencias externas.
- Manejar estructuras de datos en memoria.
- Importar y exportar archivos con formato CSV personalizado.

Formato de datos requerido por el proyecto (orden obligatorio de columnas):
1) nit
2) nombre_empresa
3) direccion
4) presupuesto_anual

Separador de campos: |
Separador de registros: salto de linea (enter)

Ejemplo de linea valida:
900123456|Mi Empresa S.A.S|Calle 10 # 20-30|35000000.5
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


# La clase Empresa representa un registro de nuestra "tabla" empresa.
# Usamos @dataclass para reducir codigo repetitivo y mantenerlo claro.
@dataclass
class Empresa:
    nit: str
    nombre_empresa: str
    direccion: str
    presupuesto_anual: float


class GestorEmpresas:
    """
    Esta clase centraliza toda la logica CRUD sobre una lista en memoria.

    En una base de datos real tendriamos tablas y sentencias SQL.
    Aqui usamos una lista para fines educativos.
    """

    def __init__(self) -> None:
        self.empresas: list[Empresa] = []

    def buscar_por_nit(self, nit: str) -> Empresa | None:
        """Devuelve la empresa con ese NIT o None si no existe."""
        for empresa in self.empresas:
            if empresa.nit == nit:
                return empresa
        return None

    def adicionar(self, empresa: Empresa) -> bool:
        """
        Inserta un nuevo registro.
        Retorna True si se inserto, False si el NIT ya existe.
        """
        if self.buscar_por_nit(empresa.nit):
            return False
        self.empresas.append(empresa)
        return True

    def eliminar(self, nit: str) -> bool:
        """
        Elimina por NIT.
        Retorna True si elimino, False si no encontro el registro.
        """
        empresa = self.buscar_por_nit(nit)
        if not empresa:
            return False
        self.empresas.remove(empresa)
        return True

    def consultar(self, nit: str) -> Empresa | None:
        """Consulta individual por NIT."""
        return self.buscar_por_nit(nit)

    def actualizar(self, nit: str, nombre: str, direccion: str, presupuesto: float) -> bool:
        """
        Actualiza los datos de una empresa existente por NIT.
        Retorna True si actualizo, False si no encontro el registro.
        """
        empresa = self.buscar_por_nit(nit)
        if not empresa:
            return False

        empresa.nombre_empresa = nombre
        empresa.direccion = direccion
        empresa.presupuesto_anual = presupuesto
        return True

    def listar(self) -> list[Empresa]:
        """Retorna todos los registros."""
        return self.empresas

    def exportar_csv(self, ruta_archivo: str) -> None:
        """
        Exporta registros al formato pedido:
        nit|nombre_empresa|direccion|presupuesto_anual

        Importante:
        - Usamos delimitador '|'.
        - Cada empresa en una nueva linea (enter).
        - Se conserva el orden de columnas solicitado.
        """
        ruta = Path(ruta_archivo)
        with ruta.open(mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, delimiter="|", lineterminator="\n")
            for e in self.empresas:
                escritor.writerow([e.nit, e.nombre_empresa, e.direccion, e.presupuesto_anual])

    def importar_csv(self, ruta_archivo: str) -> tuple[int, int]:
        """
        Importa registros desde archivo con separador '|'.

        Reglas aplicadas:
        - Debe haber exactamente 4 columnas por linea.
        - El presupuesto debe ser numerico.
        - Si un NIT ya existe, se omite (evita duplicados).

        Retorna: (registros_insertados, registros_omitidos)
        """
        ruta = Path(ruta_archivo)
        insertados = 0
        omitidos = 0

        with ruta.open(mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo, delimiter="|")
            for fila in lector:
                if not fila:
                    # Si hay linea vacia, se ignora.
                    continue

                if len(fila) != 4:
                    omitidos += 1
                    continue

                nit, nombre, direccion, presupuesto_txt = [campo.strip() for campo in fila]

                try:
                    presupuesto = float(presupuesto_txt)
                except ValueError:
                    omitidos += 1
                    continue

                if not nit:
                    omitidos += 1
                    continue

                empresa = Empresa(
                    nit=nit,
                    nombre_empresa=nombre,
                    direccion=direccion,
                    presupuesto_anual=presupuesto,
                )

                if self.adicionar(empresa):
                    insertados += 1
                else:
                    omitidos += 1

        return insertados, omitidos


def pedir_presupuesto() -> float:
    """Solicita presupuesto y valida que sea numerico."""
    while True:
        valor = input("Presupuesto anual: ").strip()
        try:
            return float(valor)
        except ValueError:
            print("Error: ingrese un numero valido para el presupuesto.")


def mostrar_empresa(e: Empresa) -> None:
    """Imprime una empresa en formato legible."""
    print(f"NIT: {e.nit}")
    print(f"Nombre empresa: {e.nombre_empresa}")
    print(f"Direccion: {e.direccion}")
    print(f"Presupuesto anual: {e.presupuesto_anual}")


def menu() -> None:
    """Menu principal del programa por consola."""
    gestor = GestorEmpresas()

    while True:
        print("\n=== Sistema de Empresas (Educativo) ===")
        print("1. Adicionar registro")
        print("2. Eliminar registro")
        print("3. Consultar registro")
        print("4. Actualizar registro")
        print("5. Listar todas las empresas")
        print("6. Importar desde CSV (|)")
        print("7. Exportar a CSV (|)")
        print("8. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            nit = input("NIT: ").strip()
            nombre = input("Nombre de la empresa: ").strip()
            direccion = input("Direccion: ").strip()
            presupuesto = pedir_presupuesto()

            nueva = Empresa(nit, nombre, direccion, presupuesto)
            if gestor.adicionar(nueva):
                print("Registro adicionado correctamente.")
            else:
                print("No se pudo adicionar: ya existe una empresa con ese NIT.")

        elif opcion == "2":
            nit = input("Ingrese el NIT a eliminar: ").strip()
            if gestor.eliminar(nit):
                print("Registro eliminado correctamente.")
            else:
                print("No se encontro una empresa con ese NIT.")

        elif opcion == "3":
            nit = input("Ingrese el NIT a consultar: ").strip()
            empresa = gestor.consultar(nit)
            if empresa:
                mostrar_empresa(empresa)
            else:
                print("No se encontro una empresa con ese NIT.")

        elif opcion == "4":
            nit = input("NIT de la empresa a actualizar: ").strip()
            if not gestor.consultar(nit):
                print("No se encontro una empresa con ese NIT.")
                continue

            nombre = input("Nuevo nombre de la empresa: ").strip()
            direccion = input("Nueva direccion: ").strip()
            presupuesto = pedir_presupuesto()

            gestor.actualizar(nit, nombre, direccion, presupuesto)
            print("Registro actualizado correctamente.")

        elif opcion == "5":
            empresas = gestor.listar()
            if not empresas:
                print("No hay empresas registradas.")
                continue

            print("\n--- Listado de empresas ---")
            for i, empresa in enumerate(empresas, start=1):
                print(f"\nEmpresa #{i}")
                mostrar_empresa(empresa)

        elif opcion == "6":
            ruta = input("Ruta del archivo CSV a importar: ").strip()
            try:
                insertados, omitidos = gestor.importar_csv(ruta)
                print(f"Importacion finalizada. Insertados: {insertados}. Omitidos: {omitidos}.")
            except FileNotFoundError:
                print("Error: no se encontro el archivo indicado.")
            except OSError as exc:
                print(f"Error al leer el archivo: {exc}")

        elif opcion == "7":
            ruta = input("Ruta destino del archivo CSV: ").strip()
            try:
                gestor.exportar_csv(ruta)
                print("Exportacion finalizada correctamente.")
            except OSError as exc:
                print(f"Error al escribir el archivo: {exc}")

        elif opcion == "8":
            print("Saliendo del programa...")
            break

        else:
            print("Opcion invalida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
