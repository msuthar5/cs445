//package source_packages;

public class Tiger extends Creature {
	
	public Tiger(String name){
		super(name);
	}

	//@Override
	public void move() {
		System.out.printf("%s %s has just pounced.\n", this.getName(),
														this.getClass().getSimpleName());
	}

}
