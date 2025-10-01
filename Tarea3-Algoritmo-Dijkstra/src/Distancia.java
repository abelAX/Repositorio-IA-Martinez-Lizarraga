public class Distancia {
	private int Vertice,Distancia;
	public Distancia(int Vertice,int Distancia){
		this.Vertice=Vertice;
		this.Distancia=Distancia;
	}
	public int getVertice(){
		return Vertice;
	}
	public int getDisancia(){
		return Distancia;
	}
	public String toString(){
		return Rutinas.PonCeros(Distancia, 5);
	}
}