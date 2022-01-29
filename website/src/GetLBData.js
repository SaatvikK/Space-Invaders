//require("dotenv").config();
const MongoClient = require('mongodb').MongoClient;
const SortFunc = require("./mergesort.js"); // Importing the merge-sort script so that we can sort the list of games later.

const mongoLoginDets = () => {
  // Getting the login details from `.env` and creating the URI and then returning it.
  const MongoUsername = process.env.MONGO_USERNAME;
  const MongoPassword = process.env.MONGO_PASSWORD;
  return "mongodb+srv://" + MongoUsername + ":" + MongoPassword + "@main.l6fkh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
}

// `module.exports` means that we are exporting this function, so that this function will be automatically called when we import
// the script in `index.js`.
// The `async` keyword signifies that this function will use asynchronous data transmission/execution.
// This is one of two ways that functions can be identified in JavaScript. This method is called the ES6 Arrow Notation.
// `() => {}` is the exact same as `function () {}`, where `()` are where the parameters for the function go in each method.
module.exports = async () => {

  //Get names of all DBs.
  const client = new MongoClient(mongoLoginDets(), {
    useNewUrlParser: true,
    useUnifiedTopology: true
  });

  // Use admin request
  await client.connect(); // Awaiting for a successful connection to the client.
  const dbs = await client.db("test").admin().listDatabases(); // Getting all of the databases within a project (each database is one game, and the name of each DB is the game ID).
  let AllDBs = [];

  try {
    for(let i = 0; i < dbs.databases.length; i++) { // Iterating through all the games.
      // Since one of the databases, "login", is not a game database (and therefore not a number), a check must be ran to avoid an error being thrown.
      // IF the name of the current databse IS NOT A NUMBER (i.e. if it's a word) then do not run the following lines.
      if(isNaN(dbs.databases[i].name) == false) {
        let database = dbs.databases[i].name;
        //await client.connect();
        // Getting all of the collections of the database
        const StatsCol = await client.db(database).collection("stats");
        const SettingsCol = await client.db(database).collection("settings");

        // Finding the score, difficulty, and username.
        const score = await StatsCol.findOne({"identifier": 0});
        const difficulty = await SettingsCol.findOne({"identifier": 0});
        const usrn = await SettingsCol.findOne({"identifier": 2});

        // Adding a list of the gameID, the score, difficulty, and username to AllDBs[]
        try { AllDBs.push({"GameID": database, "score": score.score, "difficulty": difficulty.difficulty, "username": usrn.username}); }
        catch {}

        // `usrn.username` is the username of the account that owns this game.
      }
    }
    AllDBs = SortFunc(AllDBs); // Sorting the list using a merge sort algorithm. As stated previously, this algorithm has a time complexity of O(n log n).
    return new Promise(function(res, rej) { // Returning a promise. 
      if(AllDBs.length > 0) res(AllDBs);
      else rej("X_X");
    });
  } catch(e) {
    console.log(e);

  } finally { client.close(); } // Closing the connection to the client.
}
