using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Cv.Web;
using Cv.Web.Services;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

// Scoped to match HttpClient's lifetime. In WebAssembly a scope lasts the whole session,
// so the document is still fetched once and shared by every renderer.
builder.Services.AddScoped<CvDataService>();

await builder.Build().RunAsync();
