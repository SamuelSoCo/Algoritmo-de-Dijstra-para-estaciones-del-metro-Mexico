"""
rangos.py

Script sencillo para calcular "rangos" entre dos conjuntos de puntos A y B.
Para cada punto p in B, su rango = número de puntos q in A tal que q.y < p.y.

Provee:
 - implementación directa (fácil de entender, O(|A| * |B|))
 - implementación eficiente (ordenar Y de A y usar búsqueda binaria, O((|A|+|B|) log |A|))
 - menú interactivo para probar y mostrar resultados
"""

from bisect import bisect_left
from typing import List, Tuple

Point = Tuple[float, float]  # (x, y)


# -----------------------------
# Implementación simple (clara)
# -----------------------------
def compute_ranks_bruteforce(A: List[Point], B: List[Point]) -> List[int]:
    """
    Para cada punto p en B cuenta cuántos puntos q en A tienen q.y < p.y.
    Complejidad: O(|A| * |B|). Muy clara pero lenta si A y B son grandes.
    """
    ranks = []
    for bx, by in B:
        count = 0
        for ax, ay in A:
            if ay < by:
                count += 1
        ranks.append(count)
    return ranks


# -----------------------------------------
# Implementación más eficiente (ordenada)
# -----------------------------------------
def compute_ranks_sorted(A: List[Point], B: List[Point]) -> List[int]:
    """
    Ordena las coordenadas Y de A y usa búsqueda binaria para contar
    cuántas Y_A < y_b para cada punto en B.
    Complejidad: ordenar O(|A| log |A|) + O(|B| log |A|) para las consultas.
    """
    # Extraer y ordenar solo las coordenadas Y de A
    y_a_sorted = sorted([ay for (_, ay) in A])
    ranks = []
    for _, by in B:
        # bisect_left devuelve la primera posición donde by podría insertarse
        # manteniendo el orden; es igual al número de elementos < by.
        count = bisect_left(y_a_sorted, by)
        ranks.append(count)
    return ranks


# -----------------------------
# Utilidades de entrada/impresion
# -----------------------------
def parse_point(text: str) -> Point:
    """Parsea 'x,y' o 'x y' a una tupla (float(x), float(y))."""
    sep = ',' if ',' in text else None
    parts = text.split(sep)
    if len(parts) == 1:
        parts = text.split()
    if len(parts) != 2:
        raise ValueError("Formato inválido. Usa 'x,y' o 'x y'.")
    return float(parts[0].strip()), float(parts[1].strip())


def print_points(points: List[Point], label: str = "Puntos"):
    print(f"\n{label} (x, y):")
    for i, (x, y) in enumerate(points):
        print(f"  [{i}] ({x}, {y})")
    print()


# -----------------------------
# Datos de ejemplo (imagen ayuda)
# -----------------------------
EXAMPLE_A = [
    (0.5, 3.0),
    (0.1, 1.0),
    (0.3, 0.2),
]

EXAMPLE_B = [
    (1.5, 3.5),
    (1.8, 1.2),
    (1.1, 0.4),
]


# -----------------------------
# Menú simple en consola
# -----------------------------
def menu():
    A = EXAMPLE_A.copy()
    B = EXAMPLE_B.copy()

    while True:
        print("\n--- Menú Rangos ---")
        print("1) Usar datos de ejemplo")
        print("2) Mostrar conjuntos A y B")
        print("3) Ingresar puntos en A (reemplaza A)")
        print("4) Ingresar puntos en B (reemplaza B)")
        print("5) Calcular rangos (método simple O(|A|*|B|))")
        print("6) Calcular rangos (método eficiente O((|A|+|B|) log |A|))")
        print("7) Salir")
        opt = input("Elige una opción: ").strip()

        if opt == '1':
            A = EXAMPLE_A.copy()
            B = EXAMPLE_B.copy()
            print("Se cargaron los datos de ejemplo.")
        elif opt == '2':
            print_points(A, "Conjunto A")
            print_points(B, "Conjunto B")
        elif opt == '3':
            A = []
            print("Ingresa puntos para A. Escribe vacío para terminar.")
            while True:
                line = input("Punto A (x,y): ").strip()
                if not line:
                    break
                try:
                    pt = parse_point(line)
                    A.append(pt)
                except Exception as e:
                    print("Error:", e)
            print("Conjunto A actualizado.")
        elif opt == '4':
            B = []
            print("Ingresa puntos para B. Escribe vacío para terminar.")
            while True:
                line = input("Punto B (x,y): ").strip()
                if not line:
                    break
                try:
                    pt = parse_point(line)
                    B.append(pt)
                except Exception as e:
                    print("Error:", e)
            print("Conjunto B actualizado.")
        elif opt == '5' or opt == '6':
            if not A:
                print("Conjunto A vacío. No se puede calcular.")
                continue
            if not B:
                print("Conjunto B vacío. No se puede calcular.")
                continue

            print_points(A, "Conjunto A (referencia)")
            print_points(B, "Conjunto B (a clasificar)")

            if opt == '5':
                ranks = compute_ranks_bruteforce(A, B)
                method = "Bruteforce O(|A|*|B|)"
            else:
                ranks = compute_ranks_sorted(A, B)
                method = "Ordenado + binsearch O((|A|+|B|) log |A|)"

            print(f"\nResultados ({method}):")
            for i, ((bx, by), r) in enumerate(zip(B, ranks)):
                print(f" Punto B[{i}] = ({bx}, {by})  =>  Rango = {r}")
        elif opt == '7':
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
