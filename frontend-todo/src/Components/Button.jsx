import React from "react";
import { useNavigate } from "react-router-dom";

export const Button = ({ label, color, onClick, navigateTo }) => {
  const navigate = useNavigate();
  const handleClick = () => {
    if (navigateTo) {
      navigate(navigateTo);
    } else if (onClick) {
      onClick();
    }
  };

  return (
    <button
      onClick={handleClick}
      className={`text-primary border p-3 rounded-md shadow-md hover:bg-gray-300 h-10 py-2 px-4 border-spacing-2 outline-offset-2 ${
        color === "black"
          ? "bg-black text-white hover:bg-gray-800"
          : "bg-white text-black hover:bg-gray-200"
      }`}
    >
      {label}
    </button>
  );
};
