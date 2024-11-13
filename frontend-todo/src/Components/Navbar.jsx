import React from "react";
import { Button } from "rsuite";

const Navbar = () => {
  return (
    <div className="flex justify-between items-center h-24 m-w-[1240px] px-4 mx-auto text-[#e17ec5]">
      <h1 className="w-full text-3xl font-bold text-[#e17ec5]">ToDo</h1>
      <ul className="flex space-x-4">
        <Button appearance="ghost" color="blue">
          Login
        </Button>
        <Button appearance="ghost" color="green">
          Sign Up
        </Button>
      </ul>
    </div>
  );
};

export default Navbar;
