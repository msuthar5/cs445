package button;

import light_bulbs.LightBulb;

public class PushDownButton extends Button {
	
	/**
	 * Call the superclass constructor who, will initialize the
	 * variables: isOn and location
	 */
	public PushDownButton(String location) {
		super(location);
	}
	/**
	 * Function that takes an operation as input and performs the action
	 * if the input is valid.
	 * 
	 * If on_or_off called with anything other than ON or OFF, then print error message
	 * 
	 * @param on_or_off: the operation to perform on the switch. either 'ON' or 'OFF' or any camlecase combination of them
	 * 
	 */
	public void pushButton(String on_or_off){
		if (on_or_off.equalsIgnoreCase("ON")){
			// call superclass function
			super.switchOn();
		}
		else if (on_or_off.equalsIgnoreCase("OFF")){
			// call superclass function
			super.switchOff();
		}
		else
			System.out.println("Must call pushButton() with: 'ON' or 'OFF' or any camlecase combination of them\n");
	}
}
