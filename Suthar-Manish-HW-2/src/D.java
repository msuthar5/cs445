public class D extends B{
	
	F[] listofF = new F[5];
	
	public D(String name){
		super(name);
	}
	
	
	public void printF(){
		
		for (int i = 0; i < listofF.length; i++){
			System.out.println(listofF[i].name);
		}
	}
}