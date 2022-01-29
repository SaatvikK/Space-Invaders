const MongoClient = require("mongodb").MongoClient;
const CryptoJS = require("crypto-js");

class user {
  constructor(InputtedUsername, InputtedPassword) { // This is equivalent to the `.__init__()` method in Python.
    [this.username, this.password] = [InputtedUsername, InputtedPassword];
  }
  
  mongoLogin(uri) {
    return new MongoClient(uri, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
  }  

  async register(uri) { // Registering a new user by adding them to the database.
    const mongo = this.mongoLogin(uri);
    try {
      await mongo.connect();
      let database = "";
      try { database = await mongo.db("login"); console.log("Connected to DB") } 
      catch(e) { return {result:false, reason:"Could not connect to MongoDB."}; }
      
      const collection = await database.collection(this.username);
      const result = await collection.insertOne({
        username: String(this.username),
        pwd: String(CryptoJS.SHA512(this.password))
      });
    } catch(e) {
      console.log("user.js err")
      console.log(e)
    } finally { mongo.close(); }
  }
  
  async login(uri) {
    const mongo = this.mongoLogin(uri);
    try {
      await mongo.connect();
      let database = "";
      try { database = await mongo.db("login"); console.log("Connected to DB") } catch(e) { 
        return {result:false, reason:"School has not been added to the DB"};
      }
      const hashedpwd = String(CryptoJS.SHA512(this.password));
      const collection = await database.collection(this.username);
      const res = await collection.findOne({"username": String(this.username)});
      if(res == null || !res) return {"result": false, reason: "Username incorrect."};
      if(hashedpwd != res.pwd) return {"result": false, reason:"Password incorrect."};
      else if(res.pwd == hashedpwd) return {"result": true};

    } catch(e) {
      console.log("user.js err")
      console.log(e)
    } finally { mongo.close(); }
  }
}

module.exports = user;