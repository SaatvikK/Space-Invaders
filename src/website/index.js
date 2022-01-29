//--------- IMPORT MODULES ---------\\
//Modules
//require("dotenv").config();
const express = require("express");
const app = express();
const path = require("path");
const port = 3000;
const logger = require("morgan");
const MongoClient = require("mongodb").MongoClient;
const CookieParser = require("cookie-parser");
const session = require("express-session");

//Files
const GetLBData = require("./src/GetLBData.js");
const user = require("./src/user.js");
//-----------------------------------\\
// Getting the MongoDB username and password from the `.env` file.
const MongoUsername = process.env.MONGO_USERNAME;
const MongoPassword = process.env.MONGO_PASSWORD;
const uri = "mongodb+srv://" + MongoUsername + ":" + MongoPassword + "@main.l6fkh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";


//----- Initialize Express Server -----\\
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// This allows the server to host multiple different sessions with each client logged into a different account.
app.use(CookieParser()); app.use(session({secret: "Shh, it's a secret!"}));

app.use(logger("dev"));

// Signifying that ExpressJS will use EJS files instead of plain HTML.
// EJS is based on HTML. However, it is able to use embedded javascript within the HTML tags to allow for dynamic generation of HTML text.
// Embedded javascript is identified using the `<% [js here] %>` tag.
app.set("view engine", "ejs");

// The server will listen on port 3000 for any requests.
app.listen(port, function() {
  console.log("Server running on port " + port);
});
//-------------------------------------\\

const CurrentUsers = {}; // Dictionary of currently logged-in clients.

// Here the GET method is being used to render `leaderboard.ejs` onto the webpage.
app.get("/leaderboard", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) // If the current client has successfully logged in.
    GetLBData().then(result => { // Get the data from the MongoDB server
      result = result.reverse(); // Reverse the sorted list of game data.
      res.render("leaderboard", {data: result}); // And render it alongside the HTML.
    });
  else res.redirect("login"); // If the current client is not logged in, then redirect them to the login page.
});

// GETTING the login page.
app.get("/login", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) // If the current client has successfully logged in.
    res.redirect("dashboard"); // Redirect them to the dashboard page, as logged in clients should not be able to log in again.
  else res.render("login"); // If the current client is not logged in, then render the login page.
});

// Rendering the about page.
app.get("/about", function(req, res) {
  res.render("about");
});

// Rendering the dashboard page.
app.get("/dashboard", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) { // If the current client has successfully logged in.
    GetLBData().then(result => { // Get the data from the MongoDB server
      result = result.reverse(); // Reverse the sorted list of game data.
      const username = CurrentUsers[req.sessionID].usrn; // Get the current client's account username using their session ID.
      res.render("dashboard", {"username": username, "data": result}); // Render the page.
    });
  } else res.redirect("login"); // Else redirect them to the login page.
});

// Rendering the register page.
app.get("/register", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID))
    res.redirect("dashboard")
  else res.render("register");
});

// POST - getting data from the client. Here the data is the username (req.body.RegUsername) and password (req.body.RegPassword).
app.post("/register", function(req, res) {
  let NewUser = new user(req.body.RegUsername, req.body.RegPassword); // Instantiating a new user.
  NewUser.register(uri).then(res.redirect("login")); // Registering the new user and then redirecting them to the login page.
});

// POST - getting data from the login page.
app.post("/login", function(req, res) {
  let NewUser = new user(req.body.LogInUsername, req.body.LogInPassword); // Instantiating a new user with the username and password given by the client.
  NewUser.login(uri).then(result => { // Logging them in.
    console.log(result)
    if(result.result == true) { // If they have successfully logged in,
      CurrentUsers[req.sessionID] = { // Add them to the CurrentUsers[] list.
        usrn: req.body.LogInUsername,
        SessionID: req.sessionID
      };
      console.log(CurrentUsers)
      res.redirect("leaderboard"); // Then redirect them to the leaderboard page, which is now accessible.
    } else res.redirect("login"); // Else (if the the login was unsucessuful).
  });
});

// This page is displayed if the user pressed the "logout" button.
app.get("/logout", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) {
    delete CurrentUsers[req.sessionID];
    req.session.destroy();
    console.log(CurrentUsers);
    res.render("logout");
  } else res.redirect("login");
});

app.get("/", function(req, res) {
  res.redirect("about");
});