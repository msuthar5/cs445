import java.util.Scanner;

public class Driver{
	
	public static void demonstrateUML(){
		System.out.println("This is a demonstration to show that the functionality of my class follows the provided UML");
		System.out.println("Generating Objects...");
		System.out.println("");
		
		A a1 = new A("ObjectA1");
		B b1 = new B("ObjectB1");
		C c1 = new C("ObjectC1");
		D d1 = new D("ObjectD1");
		E e1 = new E("ObjectE1");
		F f1 = new F("ObjectF1");
		
		System.out.println("Demonstrating the dependency between A and B");
		a1.demonstrateDependency();
		System.out.println("");
		System.out.println("Demonstrating the dependency between C and D");
		c1.demonstrateDependency();
		System.out.println("");
		
		System.out.println("Demonstrating the Class Hierarchy");
		System.out.println("NOTE: When we print a class's name and its superclass's name, we just the method sequences:\n getClass().getSimpleName() and getClass().getSuperclass().getSimpleName()");
		System.out.println("");
		System.out.println("E is a subclass of C");
		System.out.println("E's classname: " + e1.getClass().getSimpleName() + " E's superclass name: " + e1.getClass().getSuperclass().getSimpleName());
		System.out.println("");
		System.out.println("C is a subclass of A");
		System.out.println("C's classname: " + c1.getClass().getSimpleName() + " C's superclass name: " + c1.getClass().getSuperclass().getSimpleName());
		System.out.println("");
		System.out.println("D is a subclass of B");
		System.out.println("D's classname: " + d1.getClass().getSimpleName() + " D's superclass name: " + d1.getClass().getSuperclass().getSimpleName());
		System.out.println("");
		System.out.println("Demonstrating the Associativity Between D and F");
		System.out.println("F has a list of 2 instances of D...and they're names are:");
		f1.listofD[0] = new D("ObjectD_list_elem1");
		f1.listofD[1] = new D("ObjectD_list_elem2");
		f1.printD();
		System.out.println("");
		System.out.println("D has a list of 5 instances of F...and they're names are:");
		d1.listofF[0] = new F("ObjectF_list_elem1");
		d1.listofF[1] = new F("ObjectF_list_elem2");
		d1.listofF[2] = new F("ObjectF_list_elem3");
		d1.listofF[3] = new F("ObjectF_list_elem4");
		d1.listofF[4] = new F("ObjectF_list_elem5");
		d1.printF();
		System.out.println("");
	}
	
	public static void demonstrateRangedRandom(){
		
		Scanner in = new Scanner(System.in);
		System.out.println("Enter a min value for the range");
		int min = in.nextInt();
		System.out.println("Enter a max value for the range");
		int max = in.nextInt();
		in.close();
		System.out.println("");
		ImprovedRandom improvedRandom = new ImprovedRandom();
		System.out.println(improvedRandom.randomBetweenRange(min, max));
		System.out.println(improvedRandom.randomBetweenRange(min, max));
		System.out.println(improvedRandom.randomBetweenRange(min, max));
		
	}
	
	public static void demonstrateStringTokenizer(){
		
		Scanner inp = new Scanner(System.in);
		System.out.println("Enter a String: ");
		String input = inp.nextLine();
		
		ImprovedStringTokenizer improvedStringTokenizer = new ImprovedStringTokenizer(input);
		String[] wordsArray = improvedStringTokenizer.getStringAsList();
		
		System.out.println("You entered: " + input);
		for (int i = 0; i < wordsArray.length; i++){
			System.out.println("Element " + i + " of the words array is: " + wordsArray[i]);
		}
		
	}
	
	public static void main(String[] args){
		
		System.out.println("For #2:");
		demonstrateUML();
		
		System.out.println("Demonstrating the ImprovedStringTokenizer");
		System.out.println("You will be prompted for 3 strings, and will see the magic of the method that returns a list of the words in the string you enter");
		for (int a = 0; a < 3; a ++){
			demonstrateStringTokenizer();
		}
		
		System.out.println("Demonstrating the Ranged Random Number Generator");
		System.out.println("You will be prompted for a range and will be returned with 3 random numbers within that range");
		System.out.println("");
		System.out.println("NOTE: The ranges are inclusive. So min=3, max=12 will return a number x such that 3 <= x <= 12");
		System.out.println("");
		demonstrateRangedRandom();
		
		
		
	}
	
}