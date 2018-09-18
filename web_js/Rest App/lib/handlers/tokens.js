/**
 * 
 * token handlers
 * 
 */


// depedencies
var _data = require("./../data")
var helpers = require("./../helpers")

 // Tokens
tokens = (data,callback)=>{
    var acceptableMethods = ['post','get','put','delete'];
    if(acceptableMethods.indexOf(data.method.toLowerCase())>-1){
        _tokens[data.method.toLowerCase()](data,(statusCode, data)=>{

            callback(statusCode,data)
        })
    }else{
        callback(405);
    }
}

// container for all the token menthods
_tokens = {}




// define handlers for token
// to create token
// required fields -- phone, password
// optional fields -- none
_tokens.post = (data,callback)=>{
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
_tokens.get = (data,callback)=>{

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
_tokens.put = (data,callback)=>{

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
_tokens.delete = (data,callback)=>{

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
_tokens.verifyToken = (id,phone,callback)=>{

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


module.exports = {tokens , _tokens}