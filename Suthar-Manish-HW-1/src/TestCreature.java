//package source_packages;

import static org.junit.Assert.*;
import org.junit.Test;

public class TestCreature {
	
	static int THING_COUNT = 6;
	static int CREATURE_COUNT = 10;
	
	public  TestCreature() {}

	@Test
	public void test_thing_creation() {
		
		Thing thing = new Thing("Sparty");
		assertNotEquals(thing, null);
	}
	
	@Test
	public void test_thing_name(){
		Thing thing = new Thing("Sparty");
		assertEquals("Sparty", thing.getName());
	}
	
	@Test
	public void test_thing_toString(){
		Thing thing = new Thing("to string works");
		assertTrue(thing.toString().equals("to string works"));
	}
	
	@Test
	public void test_tiger_superclass(){
		Tiger t1 = new Tiger("A Tiger");
		assertEquals(Creature.class.getSimpleName(), t1.getClass().getSuperclass().getSimpleName());
	}
	
	@Test
	public void test_last_eaten_Bat(){
		
		Bat b1 = new Bat("bat_that_eats");
		Ant a1 = new Ant("to_be_eaten");
		b1.eat(a1);
		
		assertTrue(b1.lastEaten == a1);
		
	}
	
	@Test
	public void test_last_eaten_Batt_null(){
		Bat b1 = new Bat("bat_that_eats");
		Thing t1 = new Thing("to_be_eaten");
		
		b1.eat(t1);
		assertNull(b1.lastEaten);
		
	}
	
	@Test
	public void test_last_eaten_Fly(){
		
		Fly fly = new Fly("fly_to_eat");
		Thing t1 = new Thing("to_be_eaten");
		
		fly.eat(t1);
		assertTrue(fly.lastEaten == t1);
		
	}
	
	@Test
	public void last_eaten_Fly_null(){
		Fly fly = new Fly("fly_to_eat");
		Ant ant = new Ant("to_be_eaten");
		fly.eat(ant);
		assertTrue(fly.lastEaten == null);
	}
	
}
