public class Choose {
    // generate all r-elements subset from the array e
    // which contians n elements. The r-elements subset
    // is stored in array a.
    public static int e[], n;
    public static int a[], r;

    public static void process(int a[]) {
        // Print the generated subset
        for (int i = 0; i < a.length; i++)
            System.out.print(a[i] + " ");
        System.out.println();
    }

    public static void choose(int b, int c) {
        // BASE CASE: If c < 0, print the selected subset stores in array
        if (c < 0)
            process(a);
        else
            // Iterate through the elements starting from index 'b'
            for (int i = b; i < n - c; i++) {
                a[c] = e[i]; // Select element and store it in a[c]
                choose(i + 1, c - 1); // Recursive call for next element
            }
    }

    public static void main(String args[]) {
        n = Integer.parseInt(args[0]); // Get user input and convert String to Integer
        r = Integer.parseInt(args[1]); 
        e = new int[n]; // Store every element
        a = new int[r]; // Store choosed element
        for (int i = 0; i < n; i++) 
            e[i] = i;

        choose(0, r - 1);
    }
}