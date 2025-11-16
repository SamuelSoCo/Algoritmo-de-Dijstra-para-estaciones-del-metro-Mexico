from bisect import bisect_left
from typing import List, Tuple

Punto = Tuple[float, float]  # (x, y)


# -----------------------------
# Implementación simple (clara)
# -----------------------------
def calcular_rangos_fuerza_bruta(ConjuntoA: List[Punto], ConjuntoB: List[Punto]) -> List[int]:
    """
    Para cada punto p en B cuenta cuántos puntos q en A tienen q.y < p.y.
    Complejidad: O(|A| * |B|). Muy clara pero lenta si A y B son grandes.
    """
    rangos = []
    for _, coordenada_y_b in ConjuntoB:
        contador = 0
        for _, coordenada_y_a in ConjuntoA:
            if coordenada_y_a < coordenada_y_b:
                contador += 1
        rangos.append(contador)
    return rangos


# -----------------------------------------
# Implementación más eficiente (ordenada)
# -----------------------------------------
def calcular_rangos_ordenado(ConjuntoA: List[Punto], ConjuntoB: List[Punto]) -> List[int]:
    """
    Ordena las coordenadas Y de A y usa búsqueda binaria para contar
    cuántas Y_A < y_b para cada punto en B.
    Complejidad: ordenar O(|A| log |A|) + O(|B| log |A|) para las consultas.
    """
    # Extraer y ordenar solo las coordenadas Y de A
    coordenadas_y_a_ordenadas = sorted([ay for (_, ay) in ConjuntoA])
    rangos = []
    for _, coordenada_y_b in ConjuntoB:
        # bisect_left devuelve la primera posición donde by podría insertarse
        # manteniendo el orden; es igual al número de elementos < by.
        contador = bisect_left(coordenadas_y_a_ordenadas, coordenada_y_b)
        rangos.append(contador)
    return rangos


# -----------------------------
# Utilidades de entrada/impresion
# -----------------------------
def parsear_punto(texto: str) -> Punto:
    """Parsea 'x,y' o 'x y' a una tupla (float(x), float(y))."""
    separador = ',' if ',' in texto else None
    partes = texto.split(separador)
    if len(partes) == 1:
        partes = texto.split()
    if len(partes) != 2:
        raise ValueError("Formato inválido. Usa 'x,y' o 'x y'.")
    return float(partes[0].strip()), float(partes[1].strip())


def imprimir_puntos(puntos: List[Punto], etiqueta: str = "Puntos"):
    """Imprime una lista de puntos con su índice."""
    print(f"\n{etiqueta} (x, y):")
    for i, (x, y) in enumerate(puntos):
        print(f"  [{i}] ({x}, {y})")
    print()


# -----------------------------
# Datos de ejemplo (imagen ayuda)
# -----------------------------
EJEMPLO_A = [
    (0.5, 3.0),
    (0.1, 1.0),
    (0.3, 0.2),
]

EJEMPLO_B = [
    (1.5, 3.5),
    (1.8, 1.2),
    (1.1, 0.4),
]


# -----------------------------
# Menú simple en consola
# -----------------------------
def menu():
    A = EJEMPLO_A.copy()
    B = EJEMPLO_B.copy()

    while True:
        print("\n--- Menú Rangos ---")
        print("1) Usar datos de ejemplo")
        print("2) Mostrar conjuntos A y B")
        print("3) Ingresar puntos en A (reemplaza A)")
        print("4) Ingresar puntos en B (reemplaza B)")
        print("5) Calcular rangos (método simple O(|A|*|B|))")
        print("6) Calcular rangos (método eficiente O((|A|+|B|) log |A|))")
        print("7) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == '1':
            A = EJEMPLO_A.copy()
            B = EJEMPLO_B.copy()
            print("Se cargaron los datos de ejemplo.")
        elif opcion == '2':
            imprimir_puntos(A, "Conjunto A")
            imprimir_puntos(B, "Conjunto B")
        elif opcion == '3':
            A = []
            print("Ingresa puntos para A. Escribe vacío para terminar.")
            while True:
                linea = input("Punto A (x,y): ").strip()
                if not linea:
                    break
                try:
                    pt = parsear_punto(linea)
                    A.append(pt)
                except Exception as e:
                    print("Error:", e)
            print("Conjunto A actualizado.")
        elif opcion == '4':
            B = []
            print("Ingresa puntos para B. Escribe vacío para terminar.")
            while True:
                linea = input("Punto B (x,y): ").strip()
                if not linea:
                    break
                try:
                    pt = parsear_punto(linea)
                    B.append(pt)
                except Exception as e:
                    print("Error:", e)
            print("Conjunto B actualizado.")
        elif opcion == '5' or opcion == '6':
            if not A:
                print("Conjunto A vacío. No se puede calcular.")
                continue
            if not B:
                print("Conjunto B vacío. No se puede calcular.")
                continue

            imprimir_puntos(A, "Conjunto A (referencia)")
            imprimir_puntos(B, "Conjunto B (a clasificar)")

            if opcion == '5':
                rangos = calcular_rangos_fuerza_bruta(A, B)
                metodo = "Fuerza Bruta O(|A|*|B|)"
            else:
                rangos = calcular_rangos_ordenado(A, B)
                metodo = "Ordenado + Búsqueda Binaria O((|A|+|B|) log |A|)"

            print(f"\nResultados ({metodo}):")
            for i, ((bx, by), r) in enumerate(zip(B, rangos)):
                print(f" Punto B[{i}] = ({bx}, {by})  =>  Rango = {r}")
        elif opcion == '7':
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()