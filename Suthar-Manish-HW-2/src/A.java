
public class A {
	String name;
	B objectB = new B("ObjectB_that_an_objectA_depends_on");
	
	public A(String name){
		this.name = name;
	}
	
	public void demonstrateDependency(){
		System.out.println("this objectA: " + this.name + " has a dependency on an objectB: " + objectB.name);
		System.out.println(objectB.name + " is also a class attribute of A");
	}
}
