public class Vertice {
	private int Vertice, 
	Distancia,
	Previo,
	Peso;// peso es para los adyacentes
	private boolean Visitado;
	private Lista<Vertice> ListaAdyacente;
	public Vertice(int Vertice){
		this.Vertice=Vertice;
		Distancia=2147000000;
		Previo=-1;
		Visitado=false;
		ListaAdyacente=new Lista<Vertice>();
		Peso=0;
	}
	public Vertice(int Vertice,int Peso){
		this.Vertice=Vertice;
		this.Peso=Peso;
		Distancia=2147000000;
		Previo=-1;
		Visitado=false;
		ListaAdyacente=null;
	}
	public String toString(){
		return Rutinas.PonCeros(Vertice, 5);
	}
	public String toString(int a){
		
		return String.format("%5d %10d  %5d %6b %5d ",Vertice,Distancia,Previo,Visitado,Peso);
	}
	public int getVertice() {
		return Vertice;
	}
	public void setVertice(int vertice) {
		Vertice = vertice;
	}
	public int getPeso() {
		return Peso;
	}
	public void setPeso(int peso) {
		Peso = peso;
	}
	public Lista<Vertice> getListaAdyacente() {
		return ListaAdyacente;
	}
	public void setListaAdyacente(Lista<Vertice> listaAdyacente) {
		ListaAdyacente = listaAdyacente;
	}

	public int getDistancia() {
		return Distancia;
	}
	public void setDistancia(int distancia) {
		Distancia = distancia;
	}
	public int getPrevio() {
		return Previo;
	}
	public void setPrevio(int previo) {
		Previo = previo;
	}
	public boolean getVisitado() {
		return Visitado;
	}
	public void setVisitado(boolean visitado) {
		Visitado = visitado;
	}
}
