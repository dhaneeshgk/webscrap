/*
 * 
 * sever related tasks
 * 
 */


//  Dependenices
var http = require('http')
var https = require('https')
var url = require('url')
var fs = require('fs')
var {StringDecoder} = require('string_decoder')
var config = require('./config')
var _data = require('./data')
var handlers = require('./handlers/handlers')
var helpers = require('./helpers')
var path = require('path')


// instaniate the server module
server = {};


// Instiating the http server
server.httpServer = http.createServer( function (req, res){
    server.unifiedServer(req,res)
});


// Instiating the https server
// server.httpsServerOptions = {
//     'key':fs.readFileSync(path.join(__dirname+'./../https/key.pem')),
//     'cert':fs.readFileSync(path.join(__dirname+'./../https/cert.pem'))
// };

// server.httpsServer = https.createServer(server.httpsServerOptions,function (req, res){
//     server.unifiedServer(req,res)
// });



// all the server logic for both http and https server

server.unifiedServer = function(req,res){

        // Get the url and parse it
        // console.log(req.url)
        var parsedUrl = url.parse(req.url,true);
    
        // Get the path
        var path = parsedUrl.pathname;
        var trimmedPath = path.replace(/^\/+|\/+$/g, '')
    
        // Get the query string as object
        var queryStringObject = parsedUrl.query;
    
        // Get the method
        var method = req.method.toUpperCase()
    
        // Get the headers
        var headers = req.headers;
    
        // Get the payload if any
        var decoder = new StringDecoder('utf-8');
        var buffer = '';
        req.on('data', function(data){
            buffer +=decoder.write(data)
        })
        req.on('end', function() {
            buffer += decoder.end()
    

            // choose the handler this request should go to, if one is not Found choose notFound handler
            var chooseHandler = typeof(server.router[trimmedPath]) !== 'undefined' ? server.router[trimmedPath] : handlers.notFound
    
            // construct the data object to be sent
            var data = {
                'trimmedPath':trimmedPath,
                'queryStringObject':queryStringObject,
                'method':method,
                'headers':headers,
                'payload':helpers.parseJsonToObject(buffer)
            }
            
            // console.log("data",data)
            // console.log("chooseHandler",chooseHandler)

            // Route the request to the handler specified in the router
            chooseHandler(data,function(statusCode,payload){
                // console.log('chooseHandler-- statusCode',statusCode)
                // use the status code defined by handler else send status code 200
                statusCode = typeof(statusCode) === 'number' ? statusCode : 200
                debugger;
                // console.log('chooseHandler-- payload',payload)
                // use the status code defined by handler else send empty object
                payload = typeof(payload) === 'object' ? payload : {}
                debugger;
                // convert the payload to string
                var payloadString = JSON.stringify(payload);
    
                // set header
                res.setHeader('Content-Type','application/json')
                // return the response
                res.writeHead(statusCode)
                // send the response
                res.end(payloadString);
    
                // console.log("returning the response : ",statusCode, payloadString )
            });
    
            // log the request path
            // console.log("Trimmed Path ", trimmedPath, "with this method ", method, "with this query string paramters ", queryStringObject, "with headers ",headers)
    
            // log the request payload
            // console.log("Request recived with this payload:", buffer);
        });    
};

// define a request router
server.router = {

    "ping" : handlers.ping,
    "users" :handlers.users,
    "tokens":handlers.tokens,
    "checks":handlers.checks

}


// init script
server.init = function(){

    // start the server
    server.httpServer.listen(config.httpPort, ()=>{
    console.log(`The Server is listening on ${config.httpPort} port under enviroment ${config.envName}`)
    })

    // start the https server
//     server.httpsServer.listen(config.httpsPort, ()=>{
//     console.log(`The Server is listening on ${config.httpsPort} port under enviroment ${config.envName}`)
// })
    
}



// server module export
module.exports = server
