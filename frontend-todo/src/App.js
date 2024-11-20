import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { HomePage } from "./Pages/Home/Home.js";
import { SignUpPage } from "./Pages/SignUp/SignUp.js";
import { LoginPage } from "./Pages/SignUp/Login.js";
import { useState } from "react";
import { Navbar } from "./Pages/Navbar/Navbar.js";
import { Tasks } from "./Pages/Tasks/Tasks.js";
import { Goals } from "./Pages/Goals/Goals.js";
import { Events } from "./Pages/Events/Events";
import { ProfilePage } from "./Pages/Profile/Profile.js";

function App() {
  const [isLogged, setIsLogged] = useState(false);
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/tasks" isLogged="true" element={[<Tasks />]}></Route>
        <Route path="/goals" isLogged="true" element={[<Goals />]}></Route>
        <Route path="/events" isLogged="true" element={[<Events />]}></Route>
        <Route
          path="/profile"
          isLogged="true"
          element={[<ProfilePage />]}
        ></Route>
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
