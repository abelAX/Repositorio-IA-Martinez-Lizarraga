public class Rutinas {
    public static String PonCeros(int valor, int tamano) {

        return String.format("%0" + tamano + "d", valor);
    }
}