import React from "react";

export const Footer = () => {
  return (
    <footer className="w-full m-2 text-center text-gray-800 text-opacity-5000">
      © {new Date().getFullYear()} TaskManager. All rights reserved.
    </footer>
  );
};
