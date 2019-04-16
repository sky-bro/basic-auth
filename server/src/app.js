const CryptoJS = require('crypto-js');
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const MongoClient = require('mongodb').MongoClient

const app = express();

// define paths for Express config
const publicPath = path.join(__dirname, '../public');

db_url = 'mongodb://localhost:27017/'

// setup static dir to serve
app.use(express.static(publicPath));
app.use(bodyParser.json());

app.post('/data', async (req, res) => {
    console.log("body", req.body);
    // let data_obj = JSON.parse(req.body);
    let username = req.body.username;
    let hash2 = req.body.hash2;
    let rand1 = req.body.rand1;
    if (username && hash2 && rand1){
        // let hash1 = database[username];
        let hash1;
        let db = await MongoClient.connect(db_url, {useNewUrlParser: true})
        let dbo = db.db('lab04');
        obj = await dbo.collection("users").findOne({username: username})
        // console.log(obj)
        hash1 = obj.hash1;
        db.close();
        console.log("hash1:", hash1)
        let hash2_new = CryptoJS.SHA256(hash1 + rand1).toString();
        console.log("hash2_new:", hash2_new)
        if (hash2_new === hash2){
            let key = hash1;
            key = CryptoJS.enc.Hex.parse(key);
            let iv = CryptoJS.lib.WordArray.random(128/8);
            // let iv = CryptoJS.enc.Hex.parse('57b2c3376422a1789e446c1dd4d80106'); 
            // var salt = CryptoJS.lib.WordArray.random(128/8);// var key128Bits = CryptoJS.PBKDF2("Secret Passphrase", salt, { keySize: 128/32 });
            res.json({
                status: 'success',
                rand2_encrypted: CryptoJS.AES.encrypt(rand1,key,{iv: iv, mode: CryptoJS.mode.CBC, padding:CryptoJS.pad.Pkcs7}).ciphertext.toString(), //default hex
                iv: iv.toString()
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