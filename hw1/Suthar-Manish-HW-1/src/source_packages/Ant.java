package source_packages;

public class Ant extends Creature {
	
	public Ant(String name){
		super(name);
	}
	
	@Override
	public void move() {
		System.out.printf("%s %s is crawling around.\n", this.getName(),
														this.getClass().getSimpleName());
		
	}

}
