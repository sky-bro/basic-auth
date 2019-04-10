// require.config({
//     paths: {
//         'crypto-js': 'path-to/bower_components/crypto-js/crypto-js'
//     }
// });
 
// require(["crypto-js"], function (CryptoJS) {
//     console.log(CryptoJS.HmacSHA1("Message", "Key"));
// });

console.log(CryptoJS.HmacSHA1("Message", "Key").toString(CryptoJS.enc.Hex));