/**
 * 
 * Library for storing and editing the data
 * 
 * 
 */

//  Dependencies 
var fs = require('fs');
var path = require('path');

// container for the module (to be exported)
var lib = {};

// base directorty for the data folder
lib.baseDir = path.join(__dirname, '/../.data/')


// write data to file
lib.create = function (dir, file, data, callback){
    // open the file for writing
    fs.open(lib.baseDir+dir+"/"+file+".json", 'wx', function (error, fileDescription){
        if (!error && fileDescription){
            // convert data to string
            var stringData = JSON.stringify(data);

            // write to file and close it
            fs.writeFile(fileDescription, stringData, function(err){
                !err ? fs.close(fileDescription, (error) => !error ? callback(false) : callback("Error while closing the function",error)) : callback('Error while writing into new file',err)
            })

        } else {
            callback('Could not create a new file, it may already exists',error)
        }   
    })
}

// read data from file
lib.read = function(dir, file, callback){
    fs.readFile(lib.baseDir+dir+"/"+file+".json",'utf8', (error,data)=>{
        // console.log(error,data)
        callback(error,helpers.parseJsonToObject(data))
    })
}


lib.update = function(dir, file, data, callback){

    // open the file for writing
    fs.open(lib.baseDir+dir+"/"+file+".json", 'r+', function (error, fileDescription){
        if (!error && fileDescription){
            // convert data to string
            var stringData = JSON.stringify(data);
            // console.log(fileDescription)
            fs.truncate(fileDescription, function(err){
                if(!err){
                     // write to file and close it
                    fs.writeFile(fileDescription, stringData, function(err){
                    !err ? fs.close(fileDescription, (error) => !error ? callback(false,data) : callback("Error while closing the function",error)) : callback('Error while writing into new file',err)
                    })
                }else{
                    callback('Error truncating the file'+error)
                }
            })
        } else {
            callback('Could not update a file, it may already exists',error)
        }   
    })

}

// delete a file
lib.delete = (dir, file,  callback)=>{

    // unlink the file
    fs.unlink(lib.baseDir+dir+"/"+file+".json", (err)=> {
        if(!err){
            callback(false)
        } else{
            callback(`Error :${err}`)
        }
    })
}


// list all the items in directory
lib.list = (dir,callback)=>{

    fs.readdir(lib.baseDir+dir+"/",(err,data)=>{

        if(!err && data && data.length>0){

            var trimmedFilenames = [];
            data.forEach(function(fileName){
                trimmedFilenames.push(fileName.replace(".json",""));
            });
            callback(false,trimmedFilenames)
        }else{
            callback(err,data)
        }

    })

}

// export the lib
module.exports = lib;