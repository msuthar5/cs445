//package source_packages;


public class Bat extends Creature implements Flyer {
	
	public Bat(String name){
		super(name);
	}
	@Override
	public void eat(Thing athing){
		
		if (athing.getClass().getSuperclass().getSimpleName().equals(Creature.class.getSimpleName())){
			super.eat(athing);
		}
		else if (athing.getClass().getSimpleName().equals(Thing.class.getSimpleName())){
			System.out.printf("%s %s wont eat a %s\n", this.getName(), this.getClass().getSimpleName(), athing);
		}else {
			;
		}
	}

	@Override
	public void fly() {
		System.out.printf("%s %s is swooping through the dark.\n", this.getName(), this.getClass().getSimpleName());
		
	}

	@Override
	public void move() {
		this.fly();
	}

}
