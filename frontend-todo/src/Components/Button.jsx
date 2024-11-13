import React from "react";
import { Button as RSButton } from "rsuite";

const Button = ({ text, appearance, color }) => {
  return (
    <RSButton appearance={appearance} color={color}>
      {text}
    </RSButton>
  );
};

export default Button;
