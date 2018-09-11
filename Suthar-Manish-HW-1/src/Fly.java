//package source_packages;

public class Fly extends Creature implements Flyer {
	
	public Fly(String name){
		super(name);
	}

	public void eat(Thing athing){
		
		if (athing.getClass().getSuperclass().getSimpleName().equals(Creature.class.getSimpleName())){
			System.out.printf("%s %s wont eat a %s\n", this.getName(), this.getClass().getSimpleName(), athing);
		}
		else if (athing.getClass().getSimpleName().equals(Thing.class.getSimpleName())){
			super.eat(athing);
		}else {
			;
		}
		
	}
	
	@Override
	public void fly() {
		// TODO Auto-generated method stub
		System.out.printf("%s %s is buzzing around in flight.\n", this.getName(), this.getClass().getSimpleName());	
	}

	@Override
	public void move() {
		// TODO Auto-generated method stub
		this.fly();
		
	}

}
