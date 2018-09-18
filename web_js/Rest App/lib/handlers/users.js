/**
 * 
 * users handlers
 * 
 * 
 */

// depedencies
var _data = require("./../data")
var helpers = require("./../helpers")
var {tokens,_tokens} = require('./tokens')



users = (data,callback)=>{
    var acceptableMethods = ['post','get','put','delete'];
    if(acceptableMethods.indexOf(data.method.toLowerCase())>-1){
        _users[data.method.toLowerCase()](data,(statusCode, data)=>{
            debugger;
            callback(statusCode,data)
        })
    }else{
        callback(405);
    }
}



_users = {}

// users post
// required data : firstName, lastName, phone, password, tosAggreement
// optional data:none
_users.post = (data, callback)=>{
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
_users.get = (data, callback)=>{

    // check that phone number is valid
    var phone = typeof(data.queryStringObject.phone) == 'string' && data.queryStringObject.phone.trim().length===10 ? data.queryStringObject.phone.trim():false

    console.log()
    if (phone){
    // verify token
    _tokens.verifyToken(data.headers['token-id'], phone,(status)=>{
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
_users.put = (data, callback)=>{

        // check that all required fields are filled out
        var firstName = typeof(data.payload.firstName) == 'string' && data.payload.firstName.trim().length> 0 ? data.payload.firstName.trim():false
        var lastName = typeof(data.payload.lastName) == 'string' && data.payload.lastName.trim().length> 0? data.payload.lastName.trim():false
        var password= typeof(data.payload.password) == 'string' && data.payload.password.length>= 6 ? data.payload.password.trim():false
        var phone = typeof(data.payload.phone) == 'string' && data.payload.phone.length===10 ? data.payload.phone.trim():false
        
        if(phone){


            // verify token
            _tokens.verifyToken(data.headers['token-id'], phone,(isTokenValid)=>{

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
_users.delete = (data,callback)=>{

    // check is it valid phone number
    var phone = typeof(data.payload.phone) == 'string' && data.payload.phone.length===10 ? data.payload.phone.trim():false
    
    if (phone){

        // verify token
        _tokens.verifyToken(data.headers['token-id'], phone,(isTokenValid)=>{

            if(isTokenValid){


                _data.read('users',phone,(err, rData)=>{

                    if(!err){
        
                        _data.delete('users',phone,(err)=>{
                            if(!err){
                                // delete the each of checks asociated with it
                                var uChecks = typeof(rData.checks) === 'object' && rData.checks instanceof Array ? rData.checks:false
                                var checkToDelete = uChecks.length;

                                if(checkToDelete){
                                    var checksDeleted = 0;
                                    var checksError = false;
                                    var tokenDeleted = false;

                                    for(let checkId of uChecks){

                                        _data.delete('checks',checkId,(err)=>{
                                            if(err){
                                                // console.log('checkId',err);
                                                
                                                checksError = true;
                                            }
                                            checksDeleted++;


                                            if(checksDeleted==checkToDelete){
                                                if(checksError){
                                                    _data.delete('tokens',data.headers['token-id'],phone,(err)=>{
                                                        if(!err){
                                                            callback(500,{'Error':'unable to remove associated data--checks'})
                                                        }else{
                                                            callback(500,{'Error':'unable to remove associated data--checks, token'})
                                                        }
                                                    })
                                                    
                                                }else{
                                                    _data.delete('tokens',data.headers['token-id'],phone,(err)=>{
                                                        if(!err){
                                                            callback(202)
                                                        }else{
                                                            callback(500,{'Error':'unable to remove associated data--token'})
                                                        }
                                                    })
                                                }
                                            }
                                        })
    

                                    }
                                } else{
                                    callback(202)
                                }

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






// exports

module.exports = {users , _users}