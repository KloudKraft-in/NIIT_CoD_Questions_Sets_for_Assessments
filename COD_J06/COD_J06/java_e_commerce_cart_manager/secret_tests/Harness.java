import java.util.*;
import java.lang.reflect.*;

/* 
 * ==========================================================
 * LOCKED CODE - DO NOT MODIFY
 * ==========================================================
 */

class Item {
    private String name;
    private double price;
    private int quantity;
    private boolean isTaxable;

    public Item(String name, double price, int quantity, boolean isTaxable) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
        this.isTaxable = isTaxable;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public int getQuantity() {
        return quantity;
    }

    public boolean isTaxable() {
        return isTaxable;
    }
}

abstract class DiscountCoupon {
    protected String code;

    public DiscountCoupon(String code) {
        this.code = code;
    }

    public String getCode() {
        return code;
    }

    public abstract double getDiscount(double subtotal);
}

class InvalidCouponException extends Exception {
    public InvalidCouponException(String message) {
        super(message);
    }
}

class HarnessJ06 {
    public static void main(String[] args) {
        try {
            try (Scanner sc = new Scanner(System.in)) {
                if (!sc.hasNextInt()) return;
                int n = Integer.parseInt(sc.nextLine());

                List<Item> items = new ArrayList<>();
                for (int i = 0; i < n; i++) {
                    if (!sc.hasNextLine()) break;
                    String line = sc.nextLine();
                    String[] parts = line.split(" ");
                    if (parts.length < 4) continue;
                    
                    String name = parts[0];
                    double price = Double.parseDouble(parts[1]);
                    int qty = Integer.parseInt(parts[2]);
                    boolean isTaxable = Boolean.parseBoolean(parts[3]);
                    
                    items.add(new Item(name, price, qty, isTaxable));
                }

                if (!sc.hasNextLine()) return;
                String couponLine = sc.nextLine();
                String[] cParts = couponLine.split(" ");
                
                DiscountCoupon coupon = null;
                if (cParts.length >= 1 && !cParts[0].equalsIgnoreCase("None")) {
                    String couponType = cParts[0];
                    String code = cParts.length > 1 ? cParts[1] : "";
                    double val = 0.0;
                    if (cParts.length > 2) {
                        try {
                            val = Double.parseDouble(cParts[2]);
                        } catch (NumberFormatException e) {
                            // Leave as 0.0
                        }
                    }
                    
                    if (couponType.equalsIgnoreCase("Percentage")) {
                        Class<?> pctClass = Class.forName("PercentageDiscount");
                        Constructor<?> ctor = pctClass.getConstructor(String.class, double.class);
                        coupon = (DiscountCoupon) ctor.newInstance(code, val);
                    } else if (couponType.equalsIgnoreCase("Flat")) {
                        Class<?> flatClass = Class.forName("FlatDiscount");
                        Constructor<?> ctor = flatClass.getConstructor(String.class, double.class);
                        coupon = (DiscountCoupon) ctor.newInstance(code, val);
                    }
                }

                // Create CartService via reflection
                Class<?> serviceClass = Class.forName("CartService");
                Object service = serviceClass.getDeclaredConstructor().newInstance();
                Method calcMethod = serviceClass.getMethod("calculateTotal", List.class, DiscountCoupon.class);
                
                try {
                    double total = (double) calcMethod.invoke(service, items, coupon);
                    
                    // If no exception, print breakdown
                    double subtotal = 0;
                    double taxableSubtotal = 0;
                    for (Item item : items) {
                        double itemTotal = item.getPrice() * item.getQuantity();
                        subtotal += itemTotal;
                        if (item.isTaxable()) {
                            taxableSubtotal += itemTotal;
                        }
                    }
                    
                    double discount = 0;
                    if (coupon != null && subtotal > 0) {
                        discount = coupon.getDiscount(subtotal);
                    }
                    
                    double tax = taxableSubtotal * 0.10;
                    
                    System.out.printf(Locale.US, "Subtotal: %.2f\n", subtotal);
                    System.out.printf(Locale.US, "Discount: %.2f\n", discount);
                    System.out.printf(Locale.US, "Tax: %.2f\n", tax);
                    System.out.printf(Locale.US, "Total: %.2f\n", total);
                    
                } catch (InvocationTargetException e) {
                    Throwable cause = e.getCause();
                    if (cause instanceof InvalidCouponException) {
                        System.out.println("Error: " + cause.getMessage());
                    } else {
                        System.out.println("Execution Error: " + cause.getMessage());
                    }
                }
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
