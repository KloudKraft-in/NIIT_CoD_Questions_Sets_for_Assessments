# Java: Inventory Analytics

Implement a Java program using the Streams API to process and analyze product inventory data. The program should:

* Filter out products that are out of stock
* Calculate the total valuation of the remaining inventory
* Identify the highest-priced product in each category

**Class Description**
Complete the class `InventoryService` in the editor with the following methods:

* `double calculateTotalValue(List<Product> products)`: Uses streams to sum the `price * quantity` for all in-stock products.
* `Map<String, Product> getMostExpensiveByCategory(List<Product> products)`: Returns a map where the key is the category and the value is the `Product` with the highest price in that category.

**Product Class (Provided)**

* `String name`
* `String category`
* `double price`
* `int quantity`

**Returns**

* `double`: The total inventory value formatted to two decimal places.
* `String`: The name of the most expensive product for each category requested by the harness.

**Constraints**

* $1 \le NumberOfProducts \le 500$.
* $1.0 \le Price \le 10,000.0$.

**Input Format For Custom Testing**
The first line contains an integer $N$ denoting the number of products.
The following $N$ lines contain `{Name} {Category} {Price} {Quantity}`.

**Sample Case 0**
**Sample Input For Custom Testing**

```text
4
Laptop Electronics 1200.0 5
Mouse Electronics 25.0 10
Chair Furniture 150.0 0
Desk Furniture 300.0 2
```

**Sample Output**

```text
Total Inventory Value: 6850.00
Most Expensive (Electronics): Laptop
Most Expensive (Furniture): Desk
```

**Explanation**
The Chair is out of stock (quantity 0), so it is excluded from the total value.
Total Value = (1200 * 5) + (25 * 10) + (300 * 2) = 6000 + 250 + 600 = 6850.
Laptop is more expensive than Mouse in Electronics. Desk is the only in-stock Furniture.


**Boilerplate :**

```
// student_workspace/solution.java

import java.util.*;

/* 
 * Implement the 'InventoryService' class here using Java Streams.
 * The 'Product' class is already defined in the Harness.
 * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
 */

class InventoryService {
    public double calculateTotalValue(List<Product> products) {
        // Write your code here
        return 0;
    }

    public Map<String, Product> getMostExpensiveByCategory(List<Product> products) {
        // Write your code here
        return null;
    }
}
```


**Solution.java** :

```
// student_workspace/solution.java


import java.util.*;
import java.util.stream.*;

class InventoryService {
    public double calculateTotalValue(List<Product> products) {
        return products.stream()
                .filter(p -> p.getQuantity() > 0)
                .mapToDouble(p -> p.getPrice() * p.getQuantity())
                .sum();
    }

    public Map<String, Product> getMostExpensiveByCategory(List<Product> products) {
        return products.stream()
                .filter(p -> p.getQuantity() > 0)
                .collect(Collectors.toMap(
                        Product::getCategory,
                        p -> p,
                        (p1, p2) -> p1.getPrice() >= p2.getPrice() ? p1 : p2
                ));
    }
}

```
