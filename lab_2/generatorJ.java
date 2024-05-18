import java.security.SecureRandom;
import java.math.BigInteger;

public class Main {
    public static void main(String[] args) {
        generateSingleBinarySequence();
    }

    public static void generateSingleBinarySequence() {
        SecureRandom random = new SecureRandom();
        byte[] randomBytes = new byte[16];
        random.nextBytes(randomBytes);
        
        BigInteger bigInt = new BigInteger(1, randomBytes);
        String binaryString = bigInt.toString(2);
        
        String paddedBinaryString = String.format("%128s", binaryString).replace(' ', '0');
        
        System.out.println(paddedBinaryString);
    }
}
