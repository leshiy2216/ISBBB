import java.security.SecureRandom;
import java.math.BigInteger;

/**
 * Класс содержит основной метод для запуска приложения
 * и метод для генерации одной бинарной последовательности.
 */
public class Main {
    /**
     * Основной метод для запуска приложения.
     */
    public static void main(String[] args) {
        generateSingleBinarySequence();
    }

    /**
     * Генерирует случайную 128-битную бинарную последовательность,
     * конвертирует ее в бинарную строку и выводит дополненную бинарную строку.
     */
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