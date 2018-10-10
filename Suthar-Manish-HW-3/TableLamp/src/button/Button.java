package button;

import light_bulbs.LightBulb;

public class Button implements LightBulb {

	//Boolean variable to hold status of the lightbulb
	public boolean isOn;
	public String location;
		
	public Button(String location) {
		// Initialize the class variables
		// Location is just the name of the room to place the Button in
		this.location = location;
		this.isOn = false;
	}

	/**
	 * switchOn() method as per the instructions
	 * 
	 *	we call our implemented LightBulb's on() method as well
	 *  to indicate that the lightbulb has been successfully turned on
	 *  
	 *  so the order of print statements is: switchOn()'s print statement followed by LightBulb's on() print statement
	 *  
	 */
	public void switchOn(){
		System.out.println("\nButton switched to ON");
		this.on();
		isOn = true;
	}
	
	/**
	 * switchOff() method as per the instructions
	 * 
	 *	we call our implemented LightBulb's on() method as well
	 *  to indicate that the lightbulb has been successfully turned on
	 *  
	 *  so the order of print statements is: switchOff()'s print statement followed by LightBulb's off() print statement
	 *  
	 */
	public void switchOff(){
		System.out.println("\nButton switched to OFF");
		// call the off function of lightbulb
		this.off();
		isOn = false;
	}

	/**
	 * Overriding the interface's on() to provide a custom
	 * implementation for our own function for this type of button
	 */
	@Override
	public void on() {
		System.out.println("Lightbulb on\n");
	}
	/**
	 * Overriding the interface's off() to provide a custom
	 * implementation for our own function for this type of button
	 */
	@Override
	public void off() {
		System.out.println("Lightbulb off\n");
	}
}
