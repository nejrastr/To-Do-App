import React from "react";
import { Card } from "../../Components/shared/formElements/Card";
import { Input } from "../../Components/shared/formElements/Input";
import { Label } from "../../Components/shared/formElements/Label";
import { Button } from "../../Components/Button";
import { Footer } from "../../Components/Footer";

export const LoginPage = ({ setIsLogged }) => {
  const handleLogin = () => {
    setIsLogged(true);
  };
  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gradient-to-br from-blue-100 to-indigo-200">
      <header className="w-full flex  flex-col p-4 justify-between items-center">
        <h1 className="text-2xl font-bold text-primary">TimeManager</h1>
      </header>
      <h2 className="text-center  text-3xl font-extrabold text-primary sm:text-5xl md:text-6xl mb-8">
        We create our future by planning every day.
      </h2>
      <p className="text-gray-500 mb-5 text-xl sm:text-2x1">
        Our daily habits define who we truly are.
      </p>
      <Card>
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Login</h2>
        <p className="text-gray-400 mb-5">
          Enter your credentials to access your account.
        </p>
        <div className="mb-4">
          <Label>Username</Label>
          <Input placeholder="Enter your username" />
        </div>
        <div className="mb-6">
          <Label>Password</Label>
          <Input placeholder="Enter your password" />
        </div>

        <Button
          className="flex justify-center w-full"
          label="Login"
          color="black"
          onClick={handleLogin}
          navigateTo="/tasks"
        >
          Login
        </Button>
      </Card>
      <Footer />
    </div>
  );
};
