class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None


    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)
        # Si igal no se inserta

    
    def imprimir(self):
        self._inorden(self.raiz)
        print()

    def _inorden(self, nodo):
        if nodo is not None:
            self._inorden(nodo.izquierdo)
            print(nodo.valor, end=" ")
            self._inorden(nodo.derecho)


if __name__ == "__main__":
    arbol = ArbolBinarioBusqueda()
    valores = [50, 30, 70, 20, 40, 60, 80]

    for v in valores:
        arbol.insertar(v)

    print("Árbol en orden (in-order):")
    arbol.imprimir()
