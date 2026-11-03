// import java.util.*;

// /* 
//  * Implement the 'InventoryService' class here using Java Streams.
//  * The 'Product' class is already defined in the Harness.
//  * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
//  */

// class InventoryService {
//     public double calculateTotalValue(List<Product> products) {
//         // Write your code here
//         return 0;
//     }

//     public Map<String, Product> getMostExpensiveByCategory(List<Product> products) {
//         // Write your code here
//         return null;
//     }
// }
import java.util.*;
import java.util.stream.*;

/* 
 * Reference implementation for 'InventoryService' using Java Streams.
 */

class InventoryService {
    public double calculateTotalValue(List<Product> products) {
        if (products == null)
            return 0.0;
        return products.stream()
                .mapToDouble(p -> p.getPrice() * p.getQuantity())
                .sum();
    }

    public Map<String, Product> getMostExpensiveByCategory(List<Product> products) {
        if (products == null)
            return new HashMap<>();
        return products.stream()
                .filter(p -> p.getQuantity() > 0)
                .collect(Collectors.toMap(
                        Product::getCategory,
                        p -> p,
                        (existing, replacement) -> replacement.getPrice() > existing.getPrice() ? replacement
                                : existing));
    }
}
