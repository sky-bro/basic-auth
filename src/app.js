const CryptoJS = require('crypto-js');
const AES = require('crypto-js/aes');
const SHA256 = require('crypto-js/sha256');
const express = require('express');
const path = require('path');
const hbs = require('hbs');

const app = express();

// define paths for Express config
const publicPath = path.join(__dirname, '../public');
const viewPath = path.join(__dirname, '../templates/views');
const partialsPath = path.join(__dirname, '../templates/partials');

// setup handlebars engine and views location
app.set('view engine', 'hbs');
app.set('views', viewPath);
hbs.registerPartials(partialsPath);

// setup static dir to serve
app.use(express.static(publicPath));

let database = {
    "user01": CryptoJS.SHA256('user01'+'pass01')
}

app.get('/', (req, res) => {
    res.render('index', {
        title: 'Home'
    });
});

let port = process.env.port?process.env.port:3000;
app.listen(port, ()=>{
    console.log(`listening at port ${port}`);
})