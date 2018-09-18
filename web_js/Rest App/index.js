/*
 * 
 * Primary  file for api
 * 
 */


// Dependices
var server = require('./lib/server')


// Declare the app
var app = {};


// init function
app.init = function(){

    // Start the sever
    server.init();

}

// Execute
app.init();


// export the app
module.exports = app;
