import React from "react";

import { Button } from "../Components/Button";

export const Header = () => {
  return (
    <header className="w-full p-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-primary">TimeManager</h1>
      <div className="space-x-2">
        <Button color="white" label="Login">
          Login
        </Button>
        <Button label="Sign up" color="black">
          Sign up
        </Button>
      </div>
    </header>
  );
};
