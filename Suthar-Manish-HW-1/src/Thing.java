//package source_packages;

public class Thing {
	
	private final String name;
	
	public Thing(String name){
		this.name = name;
	}
	
	public String getName(){
		return this.name;
	}
	
	@Override
	public String toString(){
		String returnStr;
		if (this.getClass().getSimpleName().equals(Thing.class.getSimpleName())){
			returnStr = this.name;
		}
		else {
			returnStr = String.format("%s %s", this.name, this.getClass().getSimpleName());
		}
		
		return returnStr;
	}

}
