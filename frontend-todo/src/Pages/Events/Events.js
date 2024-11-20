import React from "react";
import { Navbar } from "../Navbar/Navbar";

export const Events = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-100 to-indigo-200 dark:from-gray-900 dark:to-gray-800">
      <Navbar />
      <div className="flex items-center">
        <h2>This is events page</h2>
      </div>
    </div>
  );
};
