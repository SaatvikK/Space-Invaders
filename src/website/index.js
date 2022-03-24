//--------- IMPORT MODULES ---------\\
//Modules
//require("dotenv").config();
const express = require("express");
const app = express();
const port = 3000;
const logger = require("morgan");
const MongoClient = require("mongodb").MongoClient;
const CookieParser = require("cookie-parser");
const session = require("express-session");
const fs = require("fs");
const https = require("https");
const axios = require("axios");
//Files
const GetLBData = require("./src/GetLBData_v3.js");
//-----------------------------------\\

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

function spacesWith20(UsernameSpaces) {
  const arr = [...UsernameSpaces];
  for(let i = 0; i < arr.length; i++) if(arr[i] == " ") arr[i] = "%20"
  return arr.join();
}

const CurrentUsers = {}; // Dictionary of currently logged-in clients.
const errors = {};

// Here the GET method is being used to render `leaderboard.ejs` onto the webpage.
app.get("/leaderboard", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) // If the current client has successfully logged in.
    GetLBData().then(result => { // Get the data from the database server
      result = result.reverse(); // Reverse the sorted list of game data.
      res.render("leaderboard", {data: result}); // And render it alongside the HTML.
    });
  else res.redirect("login"); // If the current client is not logged in, then redirect them to the login page.
});

// GETTING the login page.
app.get("/login", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) // If the current client has successfully logged in.
    res.redirect("dashboard"); // Redirect them to the dashboard page, as logged in clients should not be able to log in again.
  else res.render("login", { err: errors.login }); // If the current client is not logged in, then render the login page.
});

// Rendering the about page.
app.get("/about", function(req, res) {
  res.render("about");
});

app.get("/download", function (req, res) {
  res.render("download");
});

// Rendering the dashboard page.
app.get("/dashboard", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID)) { // If the current client has successfully logged in.
    GetLBData().then(result => { // Get the data from the MongoDB server
      result = result.reverse(); // Reverse the sorted list of game data.
      console.log(result)
      const username = CurrentUsers[req.sessionID].usrn; // Get the current client's account username using their session ID.
      res.render("dashboard", {"username": username, "data": result }); // Render the page.
    });
  } else res.redirect("login"); // Else redirect them to the login page.
});

// Rendering the register page.
app.get("/register", function(req, res) {
  if(Object.keys(CurrentUsers).includes(req.sessionID))
    res.redirect("dashboard")
  else res.render("register", { err: errors.register });
});

// POST - getting data from the client. Here the data is the username (req.body.RegUsername) and password (req.body.RegPassword).
app.post("/register", function(req, res) {
  const [username, password] = [req.body.RegUsername, req.body.RegPassword];
  axios.get(`https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/users/${username}/${password}`)
  .then(function (response) {
    const result = response.data;
    if(result.result == true) {
      errors.register = "Username already taken.";
      res.redirect("register");
    }
  }).catch(function (error) {
    const result = error.response.data;
    // For the API, there is no native way to check if an account already exists.
    // To save time, we can use the login GET method module.
    // In this module, the database checks if the collection exists.
    // If yes, then the account does exist. Else, a json with the message "Username incorrect." will be sent back.
    // If the website server receives that response, we can assume it to mean that the account does not yet exist.
    if(result.reason == "Username incorrect.") {
      axios.post(`https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/users/${username}/${password}`)
        .then(function (response) {
          // handle success
          const result = response.data;
          if(result.result == false) {
            errors.register = result.reason;
            res.redirect("register");
          } else {
            errors.login = null;
            res.redirect("login");
          }
        })
        .catch(function (error) {
          // handle error
          errors.register = error;
          console.log(error);
          res.redirect("register");
        }); 
    } else {
      console.log("£egdsrfggg")
      errors.register = "Username already taken.";
      res.redirect("register");
    }
  });
});

// POST - getting data from the login page.
app.post("/login", function(req, res) {
  const [username, password] = [req.body.LogInUsername, req.body.LogInPassword];
  axios.get(`https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/users/${username}/${password}`)
  .then(function (response) {
    // handle success
    const result = response.data;
    if(result.result == true) { // If they have successfully logged in,
      CurrentUsers[req.sessionID] = { // Add them to the CurrentUsers[] list.
        usrn: req.body.LogInUsername,
        SessionID: req.sessionID
      };
      console.log(CurrentUsers)
      res.redirect("leaderboard"); // Then redirect them to the leaderboard page, which is now accessible.
    } else {
      errors.login = null;
      res.redirect("login"); // Else (if the the login was unsucessuful).     
    }
  })
  .catch(function (error) {
    // handle error
    console.log(error);
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

app.get('*', function(req, res){
  res.status(404).render("404");
});