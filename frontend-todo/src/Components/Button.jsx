import React from "react";

export const Button = ({ label, color }) => {
  return (
    <button
      className={`text-primary border p-3 rounded-md shadow-md hover:bg-gray-600 h-10 py-2 px-4 border-spacing-2 outline-offset-2 ${
        color === "black"
          ? "bg-black text-white hover:bg-gray-800"
          : "bg-white text-black hover:bg-gray-200"
      }`}
    >
      {label}
    </button>
  );
};
