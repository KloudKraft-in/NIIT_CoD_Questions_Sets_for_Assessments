var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Incorrect pipeline order: static files served before authentication
app.UseStaticFiles();
app.UseAuthentication();
app.UseAuthorization();

app.Run();