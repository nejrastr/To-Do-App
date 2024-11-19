import React from "react";

export const Input = ({ placeholder }) => {
  return (
    <input
      placeholder={placeholder}
      type="text"
      className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
    ></input>
  );
};
