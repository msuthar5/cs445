import java.util.StringTokenizer;

public class ImprovedStringTokenizer extends StringTokenizer {

	public ImprovedStringTokenizer(String str) {
		super(str);
	}
	public ImprovedStringTokenizer(String str, String delim) {
		super(str, delim);
	}
	public ImprovedStringTokenizer(String str, String delim, boolean returnDelims) {
		super(str, delim, returnDelims);
	}

	public String[] getStringAsList(){

		int numWords = this.countTokens();
		String[] words = new String[numWords];
		for (int i = 0; i < numWords; i++){
			words[i] = this.nextToken();
		}

		return(words);
	}
}
