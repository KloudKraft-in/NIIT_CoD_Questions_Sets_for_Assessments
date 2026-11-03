import java.util.Scanner;

class HarnessJ01 {
    public static void main(String[] args) {
        try (Scanner scan = new Scanner(System.in)) {
            Object compObj = null;
            try {
                java.lang.reflect.Constructor<?> ctor = Class.forName("Comparator").getDeclaredConstructor();
                ctor.setAccessible(true);
                compObj = ctor.newInstance();
            } catch (Exception e) {
                System.out.println("DEBUG: Instantiation failed: " + e.toString());
            }

            if (!scan.hasNextInt()) return;
            int testCases = Integer.parseInt(scan.nextLine());
            while (testCases-- > 0) {
                if (!scan.hasNextInt()) break;
                int condition = Integer.parseInt(scan.nextLine());
                switch (condition) {
                    case 1:
                        String s1 = scan.nextLine().trim();
                        String s2 = scan.nextLine().trim();
                        if (compObj != null) {
                            try {
                                java.lang.reflect.Method m = compObj.getClass().getDeclaredMethod("compare", String.class, String.class);
                                m.setAccessible(true);
                                boolean result = (boolean) m.invoke(compObj, s1, s2);
                                System.out.println(result ? "Same" : "Different");
                            } catch (Exception e) { System.out.println("Error calling compare(String, String): " + e.getMessage()); }
                        }
                        break;
                    case 2:
                        int num1 = scan.nextInt();
                        int num2 = scan.nextInt();
                        if (compObj != null) {
                            try {
                                java.lang.reflect.Method m = compObj.getClass().getDeclaredMethod("compare", int.class, int.class);
                                m.setAccessible(true);
                                boolean result = (boolean) m.invoke(compObj, num1, num2);
                                System.out.println(result ? "Same" : "Different");
                            } catch (Exception e) { System.out.println("Error calling compare(int, int): " + e.getMessage()); }
                        }
                        if (scan.hasNextLine()) scan.nextLine();
                        break;
                    case 3:
                        int[] array1 = new int[scan.nextInt()];
                        int[] array2 = new int[scan.nextInt()];
                        for (int i = 0; i < array1.length; i++) array1[i] = scan.nextInt();
                        for (int i = 0; i < array2.length; i++) array2[i] = scan.nextInt();
                        if (compObj != null) {
                            try {
                                java.lang.reflect.Method m = compObj.getClass().getDeclaredMethod("compare", int[].class, int[].class);
                                m.setAccessible(true);
                                boolean result = (boolean) m.invoke(compObj, array1, array2);
                                System.out.println(result ? "Same" : "Different");
                            } catch (Exception e) { System.out.println("Error calling compare(int[], int[]): " + e.getMessage()); }
                        }
                        if (scan.hasNextLine()) scan.nextLine();
                        break;
                    default: break;
                }
            }
        }
    }
}
