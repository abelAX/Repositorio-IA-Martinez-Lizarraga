public class ColaD<T> {
    private Nodo<T> frente;
    private Nodo<T> fin;
    private T dr; // Dato retirado

    public ColaD() {
        frente = null;
        fin = null;
        dr = null;
    }

    public boolean Insertar(T info) {
        Nodo<T> nuevo = new Nodo<>(info);
        if (nuevo == null) {
            return false;
        }
        if (frente == null) {
            frente = fin = nuevo;
        } else {
            fin.setSig(nuevo);
            fin = nuevo;
        }
        return true;
    }

    public boolean Retirar() {
        if (frente == null) {
            return false;
        }
        dr = frente.getInfo(); // Guarda la información antes de retirar
        frente = frente.getSig();
        if (frente == null) {
            fin = null;
        }
        return true;
    }

    public T getDr() {
        return dr;
    }
}