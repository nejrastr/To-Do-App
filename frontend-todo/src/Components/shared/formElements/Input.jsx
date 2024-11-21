import React from "react";

export const Input = ({ placeholder, onChange }) => {
  const handleOnChange = (e) => {
    if (onChange) {
      onChange(e.target.value);
    }
  };
  return (
    <input
      onChange={handleOnChange}
      placeholder={placeholder}
      type="text"
      className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
    ></input>
  );
};
