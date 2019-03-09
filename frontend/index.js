
const client = new smartcar.AuthClient({
  clientId: 'e8236e6a-5e3d-4503-9b86-1e2181c6e4a8',
  clientSecret: '437e23d7-9460-471a-ba32-52a374ec92e9',
  redirectUri: 'http://localhost:5500/logged-in.html',
  scope: ['read_vehicle_info', 'read_odometer'],
  testMode: true,
});

app.get('/login', function(req, res) {
  const link = client.getAuthUrl();
  res.redirect(link);
});