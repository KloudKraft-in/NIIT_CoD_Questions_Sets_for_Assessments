import java.util.*;


class Harness {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        try {
            try (Scanner sc = new Scanner(System.in)) {
                if (!sc.hasNextInt()) return;
                int n = Integer.parseInt(sc.nextLine());
                List<Object> products = new ArrayList<>();
                Set<String> categories = new TreeSet<>();

                // Load Product class and constructor via reflection to avoid IDE errors
                Class<?> productClass = Class.forName("Product");
                java.lang.reflect.Constructor<?> productCtor = productClass.getConstructor(String.class, String.class, double.class, int.class);

                while (n-- > 0) {
                    String[] p = sc.nextLine().split(" ");
                    if (p.length < 4) continue;
                    Object prod = productCtor.newInstance(p[0], p[1], Double.parseDouble(p[2]), Integer.parseInt(p[3]));
                    products.add(prod);
                    categories.add(p[1]);
                }

                Class<?> serviceClass = Class.forName("InventoryService");
                java.lang.reflect.Constructor<?> ctor = serviceClass.getDeclaredConstructor();
                ctor.setAccessible(true);
                Object service = ctor.newInstance();

                java.lang.reflect.Method calcMethod = serviceClass.getDeclaredMethod("calculateTotalValue", List.class);
                calcMethod.setAccessible(true);
                double total = (double) calcMethod.invoke(service, products);
                System.out.printf("Total Inventory Value: %.2f\n", total);
                
                java.lang.reflect.Method expensiveMethod = serviceClass.getDeclaredMethod("getMostExpensiveByCategory", List.class);
                expensiveMethod.setAccessible(true);
                Map<String, Object> expensiveMap = (Map<String, Object>) expensiveMethod.invoke(service, products);
                
                if (expensiveMap == null && !products.isEmpty()) {
                    System.out.println("Error: getMostExpensiveByCategory returned null");
                } else if (expensiveMap != null) {
                    for (String cat : categories) {
                        Object topObj = expensiveMap.get(cat);
                        if (topObj != null) {
                            java.lang.reflect.Method getNameMethod = topObj.getClass().getMethod("getName");
                            String name = (String) getNameMethod.invoke(topObj);
                            System.out.println("Most Expensive (" + cat + "): " + name);
                        }
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Execution Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
