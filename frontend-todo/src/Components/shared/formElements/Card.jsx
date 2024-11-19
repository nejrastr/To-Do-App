import React from "react";

export const Card = ({ children }) => {
  return (
    <div className="bg-white shadow-md rounded border px-8 pt-6 pb-8 mb-4">
      {children}
    </div>
  );
};
