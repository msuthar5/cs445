//package source_packages;

public abstract class Creature extends Thing {

	public Thing lastEaten = null;
	
	public Creature(String name) {
		super(name);
		
	}
	
	public abstract void move();
	
	public void eat(Thing athing){
		lastEaten = athing;
		System.out.printf("%s has just eaten %s \n", this, athing);
	}
	
	public void whatDidYouEat(){
		if (lastEaten == null){
			System.out.printf("%s %s has had nothing to eat!\n", this.getName(), this.getClass().getSimpleName());
		}
		else {
			System.out.printf("%s %s has eaten a %s!\n", this.getName(),
														this.getClass().getSimpleName(),
														this.lastEaten);
		}
	}
	
	
	
	

}
