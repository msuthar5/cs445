package test_packages;

import static org.junit.Assert.*;
import org.junit.Test;
import button.Button;
import button.PushDownButton;

public class TestButtons {

	// test checks that the correct object type is instantiated for the Button()
	@Test
	public void testButtonGeneration() {
		Button b1 = new Button("B1");
		assertEquals(b1.getClass().getSimpleName(), Button.class.getSimpleName());
	}
	
	// test checks that the correct object type is instantiated for the PushDownButton()
	@Test
	public void testPushDownButtonGeneration() {
		PushDownButton b2 = new PushDownButton("B2");
		assertEquals(b2.getClass().getSimpleName(), PushDownButton.class.getSimpleName());
	}
	
	// test checks whether the switchOn function works properly
	@Test
	public void testSwitchOnFunction(){
		Button b3 = new Button("B3");
		b3.switchOn();
		assertTrue(b3.isOn);
		
	}
	
	// test checks whether the switchOn function works properly
	@Test
	public void testSwitchOffFunction(){
		Button b4 = new Button("B4");
		b4.switchOff();
		assertFalse(b4.isOn);	
	}
	
	// test checks to ensure faulty input to pushButton() does not render any operation on lightbulb
	@Test
	public void testErrorChecking(){
		PushDownButton b5 = new PushDownButton("B5");
		b5.pushButton("Bad input");
		assertFalse(b5.isOn);
	}

}
