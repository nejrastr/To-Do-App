import React from "react";

export const Footer = () => {
  return (
    <footer className="fixed bottom-0 text-center w-full  justify-center items-center">
      © {new Date().getFullYear()} TaskManager. All rights reserved.
    </footer>
  );
};
