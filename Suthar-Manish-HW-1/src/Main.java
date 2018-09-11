//package source_packages;

public class Main {
    
    static int THING_COUNT = 6;
    static int CREATURE_COUNT = 10;

	public static void main(String[] args){
		

		Thing[] things = new Thing[THING_COUNT];
		Creature[] creatures = new Creature[CREATURE_COUNT];
		
		String[] thing_names = new String[THING_COUNT];
		thing_names[0] = "Apple";
		thing_names[1] = "Peach, apple's best friend";
		thing_names[2] = "Superman";
		
		String[] creature_names = new String[CREATURE_COUNT];
		creature_names[0] = "A ferocious fish";
		creature_names[1] = "A Grizzly Bear";
		creature_names[2] = "Ant man";
		creature_names[3] = "Nasty Creature";
		creature_names[4] = "Fruit Fly";
		creature_names[5] = "Hungry Hog";
		creature_names[6] = "Sparty the Dog";
		creature_names[7] = "Crocodile";
		creature_names[8] = "Vegan Dinosaur";
		creature_names[9] = "Tony the Tiger";
		
		// Adding some Tiger instances to the things array
		things[0] = new Thing(thing_names[0]);
		things[1] = new Thing(thing_names[1]);
		things[2] = new Thing(thing_names[2]);
		things[3] = new Tiger("test_tiger_1");
		things[4] = new Tiger("test_tiger_2");
		things[5] = new Tiger("test_tiger_3");
		
		System.out.println("Things: \n");
		
		for (int i = 0; i < THING_COUNT; i++){
			System.out.println(things[i]);
		}
		
		creatures[0] = new Ant("Ant Man");
		creatures[1] = new Fly("Ferocious_Fly");
		creatures[2] = new Tiger("Tony_The_Tiger");
		creatures[3] = new Fly("Fruit_Fly");
		creatures[4] = new Tiger("Tiger_the_tiger");
		creatures[5] = new Bat("Future Batman");
		creatures[6] = new Bat("Hungry_bat");
		creatures[7] = new Ant("Fire_ant");
		creatures[8] = new Tiger("The man, the myth, the legend");
		creatures[9] = new Ant("fortnite_player");
		
		System.out.println("\nCreatures: \n");
		
		for (int x = 0; x < CREATURE_COUNT; x++){
			creatures[x].move();
		}
		
	}
}
