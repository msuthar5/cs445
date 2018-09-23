import static org.junit.Assert.*;
import java.lang.Math;
import org.junit.Test;

public class TestComponents {
	
	@Test
	public void test_A_B_inheritance(){
		C c1 = new C("An instance of C");
		assertEquals(c1.getClass().getSuperclass().getSimpleName(), A.class.getSimpleName());
	}
	
	@Test
	public void test_C_E_inheritance(){
		E e1 = new E("An instance of E");
		assertEquals(e1.getClass().getSuperclass().getSimpleName(), C.class.getSimpleName());
	}
	
	@Test
	public void test_D_B_inheritance(){
		D d1 = new D("An instance of D");
		assertEquals(d1.getClass().getSuperclass().getSimpleName(), B.class.getSimpleName());
	}
	
	@Test
	public void test_bidirectional_association_D_E(){
		D d1 = new D("An instance of D");
		assertEquals(d1.listofF.length, 5);
	}
	
	@Test
	public void test_bidirectional_association_F_D(){
		F f1 = new F("An instance of F");
		assertEquals(f1.listofD.length, 2);
	}
	
	/*
	 * This test method tests whether the dependency between A and B is satisfied 
	 * A is the client, and the supplier is B. So A should have an instance of B
	 * 
	 * This is a dummy check that just verifies that after generating an instance of A,
	 * it automatically comes with an instance of B without knowing anything about B or actually
	 * doing anything to acquire B
	 */
	@Test
	public void test_dependency_A_B(){
		A a1 = new A("An instance of A");
		assertEquals(a1.objectB.getClass().getSimpleName(), B.class.getSimpleName());
	}
	
	/*
	 * This test method tests whether the dependency between C and D is satisfied 
	 * C is the client, and the supplier is D. So C should have an instance of D
	 * 
	 * This is a dummy check that just verifies that after generating an instance of C,
	 * it automatically comes with an instance of D without knowing anything about D or actually
	 * doing anything to acquire D
	 */
	@Test
	public void test_dependency_C_D(){
		C c1 = new C("An instance of C");
		assertEquals(c1.objectD.getClass().getSimpleName(), D.class.getSimpleName());
	}
	
	/*
	 * This method tests the random range functionality. To do so, it will use the 
	 * hardcoded range of -55 <= x <= 55
	 * 
	 * It will assert whether the 3 numbers returned from the range is valid and actually
	 * fall within the defined ranges
	 */
	@Test
	public void test_random_range(){
		
		Boolean[] bArray = new Boolean[3];
		Boolean[] actual = {true,true,true};
		
		ImprovedRandom improvedRandom = new ImprovedRandom();
		int val1 = improvedRandom.randomBetweenRange(-55, 55);
		int val2 = improvedRandom.randomBetweenRange(-55, 55);
		int val3 = improvedRandom.randomBetweenRange(-55, 55);
		
		bArray[0] = (val1 >= -55) && (val1 <=55);
		bArray[1] = (val2 >= -55) && (val2 <=55);
		bArray[2] = (val3 >= -55) && (val3 <=55);
		assertArrayEquals(bArray, actual);
		
	}
	
	/*
	 * This method tests the method, getStringAsList() from ImprovedStringTokenizer 
	 * We use a hardcoded String and verify that the function returns the correct
	 * list representation of the string
	 * 
	 */
	@Test
	public void test_string_tokenizer_as_list(){
		String someStr = "CS445 is really  fun and I like cup of code videos";
		ImprovedStringTokenizer improvedStringTokenizer = new ImprovedStringTokenizer(someStr);
		String[] wordsArray = improvedStringTokenizer.getStringAsList();
		
		String[] actual = {"CS445", "is", "really", "fun", "and", "I", "like", "cup", "of", "code", "videos"};
		assertArrayEquals(wordsArray, actual);
	}
	
	

}
