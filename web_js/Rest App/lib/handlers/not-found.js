

// Not found handler
notFound = (data,callback)=>{
    // console.log("user is ")
    callback(404, {"message":"are you are wandering? check the links","links":["https://www.google.com/","https://www.youtube.com/"]})
}

module.exports = {notFound}