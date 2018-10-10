package driver;

import button.Button;
import button.PushDownButton;

/**
 * Driver Class to run the program
 */
public class Main {

	public static void main(String[] args) {
		
		System.out.println("\nDisplaying swithcOn() and switchOff() for the generic Button() for Part(i)");
		Button button = new Button("living room");
		button.switchOn();
		button.switchOff();
		
		System.out.println("\nDisplaying swithcOn() and switchOff() for the PushDownButton() for Part(iii)");
		PushDownButton pushDownButton = new PushDownButton("bathroom");
		pushDownButton.pushButton("ON");
		pushDownButton.pushButton("OFF");
		System.out.println("Displaying error handling for bad call to pushButton(): \n");
		pushDownButton.pushButton("O N");
	}
			
}