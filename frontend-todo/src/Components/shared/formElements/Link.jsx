import React from "react";
import { useNavigate } from "react-router-dom";

export const Link = ({ text, navigateTo }) => {
  const navigate = useNavigate();
  const handleClick = () => {
    if (navigateTo) {
      navigate(navigateTo);
    }
  };
  return (
    <a
      onClick={handleClick}
      className="text-black-500 hover:bg-gray-300 hover:text-gray-900 px-2 py-2 rounded-md text-sm font-medium shadow-md-blue"
    >
      {text}
    </a>
  );
};
