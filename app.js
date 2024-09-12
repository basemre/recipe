const express = require('express');
const app = express();

const authRoutes = require('./routes/auth');
const auth = require('./middleware/auth');

app.use('/auth', authRoutes);

// Example of a protected route
app.get('/protected', auth, (req, res) => {
  res.send('This is a protected route');
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});