public class F{
	
	String name;
	D[] listofD = new D[2];
	
	public F(String name){
		this.name = name;
	}
	
	
	public void printD(){
		
		for (int i = 0;i < listofD.length; i++){
			System.out.println(listofD[i].name);
		}
	}
	
}