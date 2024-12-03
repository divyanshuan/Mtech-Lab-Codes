import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class WordCounter {
    public static void main(String[] args) {
        String inputFile = "article.txt";
        int totalWords = 0;

        try (BufferedReader fileReader = new BufferedReader(new FileReader(inputFile))) {
            String currentLine;
            while ((currentLine = fileReader.readLine()) != null) {
                // Split the line into words using whitespace as the delimiter
                String[] wordArray = currentLine.trim().split("\\s+");
                totalWords += wordArray.length;
            }

            System.out.println("Total number of words: " + totalWords);
        } catch (IOException exception) {
            System.out.println("An error occurred while reading the file.");
            exception.printStackTrace();
        }
    }
}
