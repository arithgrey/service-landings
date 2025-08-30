fetch("http://localhost:8084/api/landings/pages/", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
  }
})
.then(response => response.json())
.then(data => console.log("✅ CORS funcionando:", data))
.catch(error => console.error("❌ Error CORS:", error));
