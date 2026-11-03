var builder = WebApplication.CreateBuilder(args);

builder.Services.AddTransient<ServiceA>();
builder.Services.AddTransient<ServiceB>();
builder.Services.AddTransient<ServiceC>();

var app = builder.Build();
app.Run();

// Circular dependency loop: A -> B -> C -> A
public class ServiceA {
    public ServiceA(ServiceB b) { }
}
public class ServiceB {
    public ServiceB(ServiceC c) { }
}
public class ServiceC {
    public ServiceC(ServiceA a) { }
}