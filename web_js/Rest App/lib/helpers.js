/**
 * 
 * Helpers for various tasks
 * 
 */

//  dependices
var crypto = require('crypto')
var config = require('./config')
var https = require('https')
var querystring = require('querystring')
//  container for the all heplers

helpers = {}

// create a SHA26 hash
helpers.hash = (str)=>{
    if(typeof(str)==="string" && str.length>0){
        var hash = crypto.createHash('sha256',config.hasingSecret).update(str).digest('hex')
        return hash
    }else{
        return false
    }

}


helpers.parseJsonToObject = (str)=>{
    try{
        var obj = JSON.parse(str)
        return obj;
    }catch(e){
        // console.log("Error while parsing",e)
        return {};
    }
}


helpers.createRandomeString = (strLength)=>{

    var strLength = typeof(strLength)==="number"?strLength:false
    if (strLength){

        // define all possible characters that could go into string
        var possibleChar = 'abcdefghijklmnopqrstuvwxyz123456790';

        // start the final string
        var str = ""
        for(i=1;i<=strLength;i++){

            // Get a random charcter from the possible character string
            var randomString = possibleChar.charAt(Math.floor(Math.random()* possibleChar.length))

            str+=randomString
        }
        return str
    }
    return false

}


// send a message from twilio
helpers.sendTwilioSms = function(phone,msg,callback){

    // validate parameters
    phone = typeof(phone)=='string' && phone.trim().length == 10 ? phone.trim() :false;
    msg = typeof(msg)=='string' && msg.trim().length > 0 && msg.trim().length <=1600 ?  msg.trim() :false;

    if(phone && msg){
        // conifgure the request payload
        var payload = {
            'From':config.twilio.fromPhone,
            'To':'+91'+phone,
            'Body': msg
        }


        // stringify the payload
        var stringPayload = querystring.stringify(payload);

        // configure request details
        var requestDetails = {

            'protocol': 'https:',
            'hostname':'api.twilio.com',
            'method':'POST',
            'path':'/2010-04-01/Accounts/'+config.twilio.accountsId+'/Messages.json',
            'auth':config.twilio.accountsId+' : '+ config.twilio.authToken,
            'headers':{
                'Content-Type':'application/x-www-form-urlencoded',
                'Content-Length':Buffer.byteLength(stringPayload)
            }
        }

        // Instantiate the request object
        var req = https.request(requestDetails, function(res){
            //grab the status code
            var status = res.statusCode;
            // callback successfully if request went thru
            if(status===200 || status === 201){
                callback(false)
            }else{
                callback('Status code returned was '+status)
            }
        })

        // Bind to the error event so it doesnot get thrown
        req.on('error',(e)=>{
            callback(e)
        })


        // add the payload
        req.write(stringPayload)

        // end the request
        req.end();

    }else{

        callback('Given parameters were missing or invalid')
    }

}

// export the modules
module.exports = helpers