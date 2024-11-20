import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { HomePage } from "./Pages/Home/Home.js";
import { SignUpPage } from "./Pages/SignUp/SignUp.js";
import { LoginPage } from "./Pages/SignUp/Login.js";
import { useState } from "react";
import { Navbar } from "./Pages/Navbar/Navbar.js";
import { Tasks } from "./Pages/Tasks/Tasks.js";

function App() {
  const [isLogged, setIsLogged] = useState(false);
  return (
    <Router>
      {isLogged && <Navbar />}

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/tasks" element={[<Navbar />, <Tasks />]}></Route>
        <Route
          path="/signup"
          setState="true"
          element={<SignUpPage setIsLogged={setIsLogged} />}
        />
        <Route
          path="/login"
          setState="true"
          element={<LoginPage setIsLogged={setIsLogged} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
