// server.js
const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();

// MongoDB connection URI
const uri = 'mongodb://localhost:27017'; // Update with your MongoDB connection URI
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

// Connect to MongoDB
client.connect(err => {
    if (err) {
        console.error('Failed to connect to MongoDB:', err);
        return;
    }
    console.log('Connected to MongoDB');

    const db = client.db('your_database_name'); // Replace 'your_database_name' with your actual database name
    const restaurantsCollection = db.collection('restaurants'); // Replace 'restaurants' with your actual collection name

    // Route to render HTML page with restaurant data
    app.get('/', async (req, res) => {
        try {
            // Retrieve restaurant data from MongoDB
            const restaurants = await restaurantsCollection.find({}).toArray();
            // Render HTML template with restaurant data
            res.render('index', { restaurants });
        } catch (err) {
            console.error('Failed to fetch restaurant data:', err);
            res.status(500).send('Internal Server Error');
        }
    });
});

// Start the server
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

