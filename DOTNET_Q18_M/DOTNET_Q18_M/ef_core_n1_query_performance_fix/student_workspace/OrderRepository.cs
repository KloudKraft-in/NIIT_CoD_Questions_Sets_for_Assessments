using System.Collections.Generic;
using System.Linq;
using Microsoft.EntityFrameworkCore;

public class OrderRepository {
    private readonly SalesDbContext _context;
    public OrderRepository(SalesDbContext context) {
        _context = context;
    }

    public List<Order> GetRecentOrders() {
        // N+1 Query bug: fetches orders, then loops to fetch order lines individually
        var orders = _context.Orders.ToList();
        foreach (var order in orders) {
            order.OrderLines = _context.OrderLines.Where(l => l.OrderId == order.Id).ToList();
        }
        return orders;
    }
}

public class Order {
    public int Id { get; set; }
    public List<OrderLine> OrderLines { get; set; }
}
public class OrderLine {
    public int Id { get; set; }
    public int OrderId { get; set; }
}
public class SalesDbContext : DbContext {
    public DbSet<Order> Orders { get; set; }
    public DbSet<OrderLine> OrderLines { get; set; }
}
