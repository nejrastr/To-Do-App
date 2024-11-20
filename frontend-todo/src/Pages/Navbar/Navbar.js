import React from "react";

import { Link } from "../../Components/shared/formElements/Link.jsx";

export const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="w-full p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-primary">TaskManager</h1>
        <div className="flex items-center justify-center ml-10">
          <div className="space-x-10 items-center flex">
            <Link text="Tasks" navigateTo="/tasks" />
            <Link text="Events" navigateTo="/events" />
            <Link text="Goals" navigateTo="/goals" />
          </div>
        </div>
        <div>
          <Link
            navigateTo="/profile"
            text="Profile"
            className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:bg-gray-200 hover:text-gray-900"
          ></Link>
        </div>
      </div>
    </nav>
  );
};
