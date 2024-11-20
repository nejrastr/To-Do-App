import React from "react";
import { Card } from "../../Components/shared/formElements/Card";
import { Input } from "../../Components/shared/formElements/Input";
import { Label } from "../../Components/shared/formElements/Label";
import { Button } from "../../Components/Button";
import { Footer } from "../../Components/Footer";

export const SignUpPage = ({ setIsLogged }) => {
  const handleSignUp = () => {
    setIsLogged(true);
  };
  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gradient-to-br from-blue-100 to-indigo-200">
      <header className="w-full flex-col p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-primary">TimeManager</h1>
      </header>
      <h2 className="text-center  text-3xl font-extrabold text-primary sm:text-5xl md:text-6xl mb-8">
        We create our future by planning every day.
      </h2>
      <p className="text-gray-500 mb-5 text-xl sm:text-2x1">
        Our daily habits define who we truly are.
      </p>
      <Card>
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Sign up</h2>
        <p className="text-gray-400 mb-5">Create your account.</p>
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
          label="Sign up"
          color="black"
          onClick={handleSignUp}
          navigateTo="/tasks"
        >
          Sign up
        </Button>
      </Card>
      <Footer />
    </div>
  );
};
