var builder = WebApplication.CreateBuilder(args);

// Captive Lifetime Bug:
// ServiceSingleton (Singleton) is registered and depends on ServiceScoped (Scoped)
builder.Services.AddSingleton<ServiceSingleton>();
builder.Services.AddScoped<ServiceScoped>();

var app = builder.Build();
app.Run();

public class ServiceScoped { }
public class ServiceSingleton {
    public ServiceSingleton(ServiceScoped scoped) { }
}