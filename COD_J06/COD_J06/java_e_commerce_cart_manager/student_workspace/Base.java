import java.util.*;

public class Item {
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

public abstract class DiscountCoupon {
    protected String code;

    public DiscountCoupon(String code) {
        this.code = code;
    }

    public String getCode() {
        return code;
    }

    public abstract double getDiscount(double subtotal);
}

public class InvalidCouponException extends Exception {
    public InvalidCouponException(String message) {
        super(message);
    }
}

public class PercentageDiscount extends DiscountCoupon {
    private double percentage;

    public PercentageDiscount(String code, double percentage) {
        super(code);
        this.percentage = percentage;
    }

    public double getPercentage() {
        return percentage;
    }

    @Override
    public double getDiscount(double subtotal) {
        return subtotal * (percentage / 100.0);
    }
}

public class FlatDiscount extends DiscountCoupon {
    private double amount;

    public FlatDiscount(String code, double amount) {
        super(code);
        this.amount = amount;
    }

    public double getAmount() {
        return amount;
    }

    @Override
    public double getDiscount(double subtotal) {
        return Math.min(amount, subtotal);
    }
}

public class CartService {

    public double calculateTotal(List<Item> items, DiscountCoupon coupon)
            throws InvalidCouponException {

        double subtotal = 0.0;
        double taxableSubtotal = 0.0;

        for (Item item : items) {
            double itemTotal = item.getPrice() * item.getQuantity();
            subtotal += itemTotal;

            if (item.isTaxable()) {
                taxableSubtotal += itemTotal;
            }
        }

        // TC9: Empty cart returns immediately
        if (subtotal == 0.0) {
            return 0.0;
        }

        if (coupon != null) {

            if (coupon.getCode() == null ||
                coupon.getCode().trim().isEmpty()) {
                throw new InvalidCouponException(
                    "Coupon code cannot be empty."
                );
            }

            if (coupon instanceof PercentageDiscount) {
                double percentage =
                    ((PercentageDiscount) coupon).getPercentage();

                if (percentage < 0 || percentage > 100) {
                    throw new InvalidCouponException(
                        "Invalid discount value."
                    );
                }
            }

            if (coupon instanceof FlatDiscount) {
                double amount =
                    ((FlatDiscount) coupon).getAmount();

                if (amount < 0) {
                    throw new InvalidCouponException(
                        "Invalid discount value."
                    );
                }
            }
        }

        double discount = 0.0;

        if (coupon != null) {
            discount = coupon.getDiscount(subtotal);
        }

        double tax = taxableSubtotal * 0.10;

        return subtotal - discount + tax;
    }
}
