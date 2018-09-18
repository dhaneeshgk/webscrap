/*
 * 
 * create and configuartion variables
 * 
 * 
 */

//  Conatiner for all environments
var environments = {};


// staging (defualt) environments
environments.staging = {
    "httpPort":1100,
    "httpsPort": 2000,
    "envName": "staging",
    "hashingSecret":"thisIsstagingSecret",
    "maxChecks":5,
    "twilio":{
        'accountsId' : 'ACb32d411ad7fe886aac54c665d25e5c5d',
        'authToken' : '9455e3eb3109edc12e3d8c92768f7a67',
        'fromPhone' : '+15005550006'
      }
}


// production environments

environments.production = {
    "httpPort": 4700,
    "httpsPort":2900,
    "envName": "prodcution",
    "hashingSecret":"thisIsprodSecret",
    "maxChecks":5,
    "twilio":{
        "accountsId":'',
        "authToken":'',
        "fromPhone":''
    }
}

// determine which environment was passed as command-line arguments
var currentEnv = typeof(process.env.NODE_ENV) == 'string' ? process.env.NODE_ENV : '';

// check the current environment is one of the environments above, if not, defualt to staging
let envToExport = typeof(environments[currentEnv])=='object' ? environments[currentEnv] : environments.staging;

// export the environments
module.exports = envToExport;