var builder = WebApplication.CreateBuilder(args);

// Standard Context registration (triggers context recreation per scope)
builder.Services.AddDbContext<SalesDbContext>();

var app = builder.Build();
app.Run();

public class SalesDbContext : Microsoft.EntityFrameworkCore.DbContext {
    public SalesDbContext(Microsoft.EntityFrameworkCore.DbContextOptions<SalesDbContext> options) : base(options) { }
}