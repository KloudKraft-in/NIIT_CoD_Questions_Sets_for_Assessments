import java.util.*;

class PercentageDiscount extends DiscountCoupon {
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

class FlatDiscount extends DiscountCoupon {
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

class CartService {
    public double calculateTotal(List<Item> items, DiscountCoupon coupon) throws InvalidCouponException {
        double subtotal = 0;
        double taxableSubtotal = 0;

        if (items != null) {
            for (Item item : items) {
                double itemTotal = item.getPrice() * item.getQuantity();
                subtotal += itemTotal;
                if (item.isTaxable()) {
                    taxableSubtotal += itemTotal;
                }
            }
        }

        // If subtotal is 0, total cost is immediately 0.0
        if (subtotal == 0) {
            return 0.0;
        }

        if (coupon != null) {
            if (coupon.getCode() == null || coupon.getCode().trim().isEmpty()) {
                throw new InvalidCouponException("Coupon code cannot be empty.");
            }
            if (coupon instanceof PercentageDiscount) {
                double pct = ((PercentageDiscount) coupon).getPercentage();
                if (pct < 0 || pct > 100) {
                    throw new InvalidCouponException("Invalid discount value.");
                }
            } else if (coupon instanceof FlatDiscount) {
                double amt = ((FlatDiscount) coupon).getAmount();
                if (amt < 0) {
                    throw new InvalidCouponException("Invalid discount value.");
                }
            }
        }

        double discount = 0;
        if (coupon != null) {
            discount = coupon.getDiscount(subtotal);
        }

        double tax = taxableSubtotal * 0.10;
        return subtotal - discount + tax;
    }
}
