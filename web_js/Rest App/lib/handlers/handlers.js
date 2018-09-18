/**
 * 
 * Request Handlers
 * 
 */




var _data = require("./../data")
var helpers = require("./../helpers")
var {users, _users }= require("./users")
var {tokens, _tokens} = require("./tokens")
var ping = require('./ping')
var notFound = require('./not-found')





// define handlers
var handlers = {}

// ping
handlers.ping = ping;

// notfound
handlers.notFound = notFound

// users
handlers.users = users;
handlers._users = _users;

// tokens
handlers.tokens = tokens
handlers._tokens = _tokens




// export handlers
module.exports = handlers






/**
 * 



// code has been modularised as above 


// dependencies
// var _data = require("./data")
// var helpers = require("./helpers")


// Users
// define users in handlres
handlers.users = (data,callback)=>{
    var acceptableMethods = ['post','get','put','delete'];
    if(acceptableMethods.indexOf(data.method.toLowerCase())>-1){
        handlers._users[data.method.toLowerCase()](data,(statusCode, data)=>{
            debugger;
            callback(statusCode,data)
        })
    }else{
        callback(405);
    }
}


handlers._users = {}



// users post
// required data : firstName, lastName, phone, password, tosAggreement
// optional data:none
handlers._users.post = (data, callback)=>{
    // check that all required fields are filled out
    var firstName = typeof(data.payload.firstName) == 'string' && data.payload.firstName.trim().length> 0 ? data.payload.firstName.trim():false
    var lastName = typeof(data.payload.lastName) == 'string' && data.payload.lastName.trim().length> 0? data.payload.lastName.trim():false
    var password= typeof(data.payload.password) == 'string' && data.payload.password.length>= 6 ? data.payload.password.trim():false
    var phone = typeof(data.payload.phone) == 'string' && data.payload.phone.length===10 ? data.payload.phone.trim():false
    var aggree = typeof(data.payload.tosAgreement) == 'boolean' && data.payload.tosAgreement ? data.payload.tosAgreement :false


    if (firstName && lastName && password && phone && aggree){


        // make user that user does not exist already
        _data.read('users', phone, (err, data)=>{

            if(err){

                // console.log("before hashing")
                // hash the password
                var hashedPassword = helpers.hash(password);

                // console.log("after hashing")
                if(hashedPassword){
                    // create the user object
                    var userObject = {
                        'firstName':firstName,
                        'lastName':lastName,
                        'phone':phone,
                        'password':hashedPassword,
                        'tosAggreement':true
                    }

                    // store data
                    _data.create('users',phone,userObject,(err,data)=>{
                        if(!err){
                            callback(200);
                        }else{
                            // console.log(err);
                            callback(500,{'Error':`${err}`});
                        }
                    });
                }else{

                    callback(500,{'Error':'Could not hash the user password'})

                }

            }else{
                // user already exist
                callback(400,{'Error':'User exist already with phone number'})
            }
        })

    }else{
        callback(400,{"Error":"Missing required fields"})
    }
}


// users get
// required field phone
// optional : none
// @TODO only let authenticated user to access their object dont let any access them
handlers._users.get = (data, callback)=>{

    // check that phone number is valid
    var phone = typeof(data.queryStringObject.phone) == 'string' && data.queryStringObject.phone.trim().length===10 ? data.queryStringObject.phone.trim():false

    console.log()
    if (phone){
    // verify token
    handlers._tokens.verifyToken(data.headers['token-id'], phone,(status)=>{
        // console.log('status',status)
        if(status){
            // lookup the user
            _data.read('users',phone, function(err,rdata){
                if(!err && rdata){
                    // remove the password before sending data
                    delete rdata.password
                    // console.log(data)
                    
                    pData = typeof(rdata)==="object"? rdata:helpers.parseJsonToObject(rdata)
                    // console.log('pData',pData)
                    callback(200,pData)

                }else{
                    callback(404)
                }
            })


        }else{
            callback(403,{'Error':'Token Id is not valid'})
        }
    })
    }
}


// users put/update
// required fields -- phone
// optional fields -- firstName, lastName, password, aggree(any on of them is required)
// @TODO only let authenticated user to update own object object dont let any update object them
handlers._users.put = (data, callback)=>{

        // check that all required fields are filled out
        var firstName = typeof(data.payload.firstName) == 'string' && data.payload.firstName.trim().length> 0 ? data.payload.firstName.trim():false
        var lastName = typeof(data.payload.lastName) == 'string' && data.payload.lastName.trim().length> 0? data.payload.lastName.trim():false
        var password= typeof(data.payload.password) == 'string' && data.payload.password.length>= 6 ? data.payload.password.trim():false
        var phone = typeof(data.payload.phone) == 'string' && data.payload.phone.length===10 ? data.payload.phone.trim():false
        
        if(phone){


            // verify token
            handlers._tokens.verifyToken(data.headers['token-id'], phone,(isTokenValid)=>{

                if(isTokenValid){

                    if( firstName || lastName || password){

                        _data.read('users',phone,(err, rData)=>{
        
                            if(!err){
        
                                rData = helpers.parseJsonToObject(rData)
        
                                rData.firstName=firstName
                                rData.lastName=lastName
        
                                _data.update('users',phone,rData,(err,data)=>{
        
                                    if (!err){
                                        delete rData.password
                                        callback(202,data)
                                    }else{
                                        console.log(err)
                                        callback(500,{'Error':'Could not update the user'})
                                    }
        
                                })
                                
        
                            }else{
                                callback(500,{'Error':err})
                            }
        
                        })
        
        
                    }else{
        
                        callback(400,{'Error':'missing fields to update'})
                    }
        

                }else{
                    callback(400,{'Error':'User authentication failed'})
                }


            });

        }else{
            callback(400,{'Error':'Missing required fields'})
        }


}

// usrers delete
// required fields -- phone
// @TODO only let an authenticated user delete the object, dont let other user to delete object
// @TODO delete any other files and other things deleted to the database
handlers._users.delete = (data,callback)=>{

    // check is it valid phone number
    var phone = typeof(data.payload.phone) == 'string' && data.payload.phone.length===10 ? data.payload.phone.trim():false
    
    if (phone){

        // verify token
        handlers._tokens.verifyToken(data.headers['token-id'], phone,(isTokenValid)=>{

            if(isTokenValid){


                _data.read('users',phone,(err, data)=>{

                    if(!err){
        
                        _data.delete('users',phone,(err)=>{
                            if(!err){
                                callback(202)
                            }else{
                                callback(500,{'Error':`Could not delete the user`})
                            }
                        })
                    }else{
                        callback(400,{'Error':`Could not find the specified user`})
                    }
                })


            }else{

                callback(400,{'Error':'User authentication failed'})

            }
        })


    }else{
        callback(400,{'Error':`Pass the valid phone number`})
    }
    
}






// Tokens
handlers.tokens = (data,callback)=>{
    var acceptableMethods = ['post','get','put','delete'];
    if(acceptableMethods.indexOf(data.method.toLowerCase())>-1){
        handlers._tokens[data.method.toLowerCase()](data,(statusCode, data)=>{

            callback(statusCode,data)
        })
    }else{
        callback(405);
    }
}

// container for all the token menthods
handlers._tokens = {}




// define handlers for token
// to create token
// required fields -- phone, password
// optional fields -- none
handlers._tokens.post = (data,callback)=>{
    // check all the fields are valid are not
    var password= typeof(data.payload.password) == 'string' && data.payload.password.length>= 6 ? data.payload.password.trim():false
    var phone = typeof(data.payload.phone) == 'string' && data.payload.phone.length===10 ? data.payload.phone.trim():false
    
    

    if(password && phone){
        // look up the user who phone number and password

        _data.read('users',phone,(err, uData)=>{
            if(!err){
                console.log('from',uData.hashedPassword)
                console.log('to',helpers.hash(password))
                if(uData.password === helpers.hash(password)){
                    // if valid create token with random and set expiration date to one hour
                    var tokenId = helpers.createRandomeString(20);
                    var expires = Date.now() +1000*60*60;
                    var tokenObject = {
                        'phone':phone,
                        'id':tokenId,
                        'expires':expires
                    }

                    // store token
                    _data.create('tokens',tokenId,tokenObject,(err)=>{
                        if(!err){
                            callback(200,tokenObject)
                        }else{
                            callback(500,{'Error':'Could not create token'})
                        }
                    })

                }else{
                    callback(400,{'Error':'User was not able to validate'})
                }
            }else{
                callback(404,{'Error':'User not found'})
            }
        })


        
    }else{
        callback(400,{'Error':'Missing required fields'})
    }


}


// to get token
// required fields -- tokenId
// optional fields -- none
handlers._tokens.get = (data,callback)=>{

    var tokenId = typeof(data.queryStringObject.id) == 'string' && data.queryStringObject.id.length===20 ? data.queryStringObject.id:false

    console.log("tokenId",tokenId)

    if(tokenId){
        _data.read('tokens',tokenId,(err, data)=>{
            if(!err){
                callback(200, data)
            }else{
                callback(404, {'Error':'Token would have expired'})
            }
        })
    }else{
        callback(400,{'Error':'Missing required details'})
    }

}



// to update token
// required fields -- id, extend
// optional fields -- none
handlers._tokens.put = (data,callback)=>{

    var tokenId = typeof(data.payload.id) == 'string' && data.payload.id.length===20 ? data.payload.id.trim():false
    var extend = typeof(data.payload.extend) == 'boolean' && data.payload.extend==true? data.payload.extend:false

    if(tokenId && extend){

        _data.read('tokens',tokenId,(err,tData)=>{

            if(!err){

                expires = tData.expires>Date.now()?Date.now() +1000*60*60:false

                if(expires){

                    _data.update('tokens',tokenId,tData,(err)=>{

                        if(!err){
                            callback(202)
                        }else{
                            callback(500, {'Error':'Error occured while updation'})
                        }
    
                    })

                }else{

                    callback(400,{'Error':'You cannot extend token as it is expired'})
                }



            }else{

                callback(404,{'Error':"Invalid token"})
            }


        })



    }else{
        callback(400,{'Error':'Missing required details'})
    }

}



// to delete token
// required fields -- id
// optional fields -- none
handlers._tokens.delete = (data,callback)=>{

    var tokenId = typeof(data.queryStringObject.id) == 'string' && data.queryStringObject.id.length===20 ? data.queryStringObject.id.trim():false
    
    if(tokenId){

        _data.delete('tokens',tokenId,(err)=>{
            if(!err){
                callback(202)
            }else{
                callback(500,{'Error':'token Id expired'})
            }
        })


    }else{
        callback(400,{'Error':'Missing required details'})
    }


}

// required fields : id phone
// optional data: none
// verify if given token is currently valid or not
// with callback
handlers._tokens.verifyToken = (id,phone,callback)=>{

    // lookup the token
    _data.read('tokens',id,(err,tData)=>{

        if(!err && tData){

            if(tData.phone===phone && tData.expires>Date.now()){
                callback(true);
            }else{
                callback(false);
            }
    
        }else{
            console.log('in else')
            callback(false);
        }
    })
}



// Ping Handler
handlers.ping = (data,callback)=>{
    callback(200);
};

// Not found handler
handlers.notFound = (data,callback)=>{
    callback(404)
}





// export handlers

module.exports = handlers

 */





