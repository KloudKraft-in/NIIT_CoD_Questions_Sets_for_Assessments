import java.util.*;


class Harness {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            // 1. Get Factory instance via reflection
            Class<?> factoryClass = Class.forName("FoodFactory");
            java.lang.reflect.Method getFactoryMethod = factoryClass.getDeclaredMethod("getFactory");
            getFactoryMethod.setAccessible(true);
            Object factory = getFactoryMethod.invoke(null);

            // 2. Register cuisines via reflection
            java.lang.reflect.Method registerMethod = factoryClass.getDeclaredMethod("registerCuisine", String.class, Class.forName("Cuisine"));
            registerMethod.setAccessible(true);

            String[] cuisineNames = {"Chinese", "Italian", "Japanese", "Mexican"};
            for (String name : cuisineNames) {
                try {
                    Class<?> cuisineClass = Class.forName(name);
                    java.lang.reflect.Constructor<?> ctor = cuisineClass.getDeclaredConstructor();
                    ctor.setAccessible(true);
                    registerMethod.invoke(factory, name, ctor.newInstance());
                } catch (Exception e) {
                    // Specific cuisine not implemented yet
                }
            }

            if (!sc.hasNextInt()) return;
            int n = Integer.parseInt(sc.nextLine());

            while (n-- > 0) {
                if (!sc.hasNextLine()) break;
                String line = sc.nextLine();
                String[] parts = line.split(" ");
                if (parts.length < 2) continue;

                String cuisineName = parts[0];
                String dishName = parts[1];

                try {
                    java.lang.reflect.Method serveMethod = factoryClass.getDeclaredMethod("serveCuisine", String.class, String.class);
                    serveMethod.setAccessible(true);
                    Object cuisine = serveMethod.invoke(factory, cuisineName, dishName);

                    if (cuisine != null) {
                        System.out.println("Serving " + dishName + "(" + cuisineName + ")");
                    } else {
                        System.out.println("Unservable cuisine " + cuisineName + " for dish " + dishName);
                    }
                } catch (Exception e) {
                    // This handles UnservableCuisineRequestException
                    System.out.println("Unservable cuisine " + cuisineName + " for dish " + dishName);
                }
            }
        } catch (Exception e) {
            // Initialization error
        } finally {
            sc.close();
        }
    }
}
