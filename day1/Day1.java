package day1;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Day1 {
    public static void main(String[] args) throws FileNotFoundException {
        File file = new File("/Users/colinwilson/Documents/GitHub/advent-of-code-2023/day1/input.txt");
        Scanner sc = new Scanner(file);

        int total = 0;

        while (sc.hasNextLine()) {
            String line = sc.nextLine();
            line = line.replaceAll("[^0-9]", "");

            String first = line.substring(0, 1);
            String last = line.substring(line.length() - 1);

            total += Integer.valueOf(first + last);
        }

        System.out.println(total);

        sc.close();
    }
}