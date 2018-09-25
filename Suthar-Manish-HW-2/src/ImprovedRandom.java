import java.util.Random;
import java.lang.Math;

public class ImprovedRandom extends Random{

	//Constructor for Random()
	public ImprovedRandom(){
		super();
	}
	//Constructor for Random(long seed)
	public ImprovedRandom(long seed){
		super(seed);
	}

	public int randomBetweenRange(int min, int max){
		return (int)((Math.random() * ((max-min))) + min); 

	}

}
