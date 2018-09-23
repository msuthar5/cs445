public class C extends A{
	
	D objectD = new D("ObjectD_that_an_objectC_depends_on");
	
	public C(String name){
		super(name);
	}
	
	public void demonstrateDependency(){
		System.out.println("this objectC: " + this.name + " has a dependency on an objectD: " + objectD.name);
		System.out.println(objectD.name + " is also a class attribute of A");
	}
	
	
}