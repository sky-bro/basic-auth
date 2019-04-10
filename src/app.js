const CryptoJS = require('crypto-js');
const AES = require('crypto-js/aes');
const SHA256 = require('crypto-js/sha256');
const express = require('express');
const bodyParser = require('body-parser');
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
app.use(bodyParser.json());

let database = {
    "sky": CryptoJS.SHA256('sky'+'pass01').toString()
}

app.get('/', (req, res) => {
    res.render('index', {
        title: 'Home'
    });
});

app.post('/data', (req, res) => {
    console.log("body", req.body);
    // let data_obj = JSON.parse(req.body);
    let username = req.body.username;
    let hash2 = req.body.hash2;
    let rand1 = req.body.rand1;
    if (username && hash2 && rand1){
        let hash1 = database[username];
        let hash2_new = CryptoJS.SHA256(hash1 + rand1).toString();
        if (hash2_new === hash2){
            res.json({
                status: 'success',
                rand2_encrypted: CryptoJS.AES.encrypt('123', hash1).toString()
                // CryptoJS.lib.WordArray.random
                // CryptoJS.AES.decrypt("U2FsdGVkX1+/3S3tj3nWXHFo7Chmm4uCDpGQFjAXBmo=", hash1).toString(CryptoJS.enc.Utf8)
            })
        } else {
            res.json({
                status: 'failed',
                error: 'authentication failed'
            })
        }
    } else {
        res.json({
            status: 'failed',
            error: "please post username, hash2, rand1 to /data"
        })
    }
});

let port = process.env.port?process.env.port:3000;
app.listen(port, ()=>{
    console.log(`listening at port ${port}`);
})