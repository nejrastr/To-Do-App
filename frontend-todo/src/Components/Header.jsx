import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../Components/Button";

export const Header = () => {
  return (
    <header className="w-full p-4 flex justify-between items-center">
      <Link to="/" className="text-2xl font-bold text-primary">
        TimeManager
      </Link>
      <div className="space-x-2">
        <Button navigateTo="/login" color="white" label="Login">
          Login
        </Button>
        <Button navigateTo="/signup" label="Sign up" color="black">
          Sign up
        </Button>
      </div>
    </header>
  );
};
