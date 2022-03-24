// THIS MODULE USES THE `HTTPS` LIBRARY TO MAKE REQUESTS.
// THIS CODE IS OUTDATED, SEE `GetLBData_v3.js` FOR REFACTORED CODE WITH THE
// AXIOS MODULE.

const SortFunc = require("./mergesort.js"); // Importing the merge-sort script so that we can sort the list of games later.
const axios = require("axios");

// `module.exports` means that we are exporting this function, so that this function will be automatically called when we import
// the script in `index.js`.
// The `async` keyword signifies that this function will use asynchronous data transmission/execution.
// This is one of two ways that functions can be identified in JavaScript. This method is called the ES6 Arrow Notation.
// `() => {}` is the exact same as `function () {}`, where `()` are where the parameters for the function go in each method.
module.exports = async () => {
  // Making a HTTPS GET request to the database to get a list of all GameIDs.
  return axios.get('https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/list')
  .then(function (response) {
    // handle success
    let result = response.data;
    console.log(result)
    if(result.result == true) {
      info = result.data.info;
      info = SortFunc(info);
      return new Promise(function(res, rej) { // Returning a promise. 
        if(info.length > 0) res(info);
        else rej("X_X");
      });
    }
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  });
}
