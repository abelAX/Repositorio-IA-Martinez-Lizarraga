public class GrafosRecorridos {
	
	ColaD<Distancia> Q=new ColaD<Distancia>();
	
	public void Dijkstra(Lista<Vertice> G, int Origen){

		if(!G.Buscar(new Vertice(Origen))){
			System.out.println("el grafo no tiene origen");
			return;
		}
		G.getDr().setDistancia(0);
		PonEnColaOrdenada(Q,new Distancia(Origen,0));

		while (Q.Retirar()){
			
			int U=Q.getDr().getVertice();
			if(!G.Buscar(new Vertice(U))){
				System.out.println("error en la estructura del grafo "+U);
				return;
			}		
			if(G.getDr().getVisitado())
				continue;
			G.getDr().setVisitado(true);
			Vertice ApU=G.getDr();
			Nodo<Vertice> Frente=G.getDr().getListaAdyacente().getFrente();
			while(Frente != null){
				int W=Frente.getInfo().getPeso();
				int VAdyacente=Frente.getInfo().getVertice();
				if(!G.Buscar(new Vertice(VAdyacente))){
					System.out.println("error en la estrutura del grafo");
					return;
				}	
				Vertice ApAd=G.getDr();
				if(! G.getDr().getVisitado()){
					Relajacion(ApU,ApAd,W);
				}	
				Frente=Frente.getSig();
			}
		}
	}
	public void Relajacion(Vertice Actual,Vertice Adyacente,int Peso){
		if(Actual.getDistancia()+Peso < Adyacente.getDistancia()){
			Adyacente.setDistancia(Actual.getDistancia()+Peso);
			Adyacente.setPrevio(Actual.getVertice());
			PonEnColaOrdenada(Q,new Distancia(Adyacente.getVertice(),Adyacente.getDistancia()));
		}
	}
	public void PonEnColaOrdenada(ColaD<Distancia> Q,Distancia  Origen){
		boolean Band=false;
		ColaD<Distancia> QAux=new ColaD<Distancia>();
		while(Q.Retirar()){
			if(Origen.toString().compareTo(Q.getDr().toString())<0 && !Band){
				Band=true;
				QAux.Insertar(Origen);
			}
			QAux.Insertar(Q.getDr());
		}
		if(!Band)
			QAux.Insertar(Origen);
		
		while(QAux.Retirar() && Q.Insertar(QAux.getDr()));
	}

}