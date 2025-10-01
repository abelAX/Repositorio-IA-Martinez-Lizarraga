public class Lista<T> {
    private Nodo<T> frente;
    private Nodo<T> fin;
    private Nodo<T> dr;

    public Lista() {
        frente = null;
        fin = null;
        dr = null;
    }

    public Nodo<T> getFrente() {
        return frente;
    }

    public Vertice getDr() {
        if (dr != null) {
            return (Vertice) dr.getInfo(); //devbuelce la infromacion dentro del nodo
        }
        return null;
    }
    public void InsertarFin(T info) {
        Nodo<T> nuevo = new Nodo<>(info);
        if (frente == null) {
            frente = fin = nuevo;
        } else {
            fin.setSig(nuevo);
            fin = nuevo;
        }
    }

    public boolean Buscar(Vertice v) {
        Nodo<T> aux = frente;
        while (aux != null) {
            if (((Vertice) aux.getInfo()).getVertice() == v.getVertice()) {
                dr = (Nodo<T>) aux;
                return true;
            }
            aux = aux.getSig();
        }
        dr = null;
        return false;
    }
}