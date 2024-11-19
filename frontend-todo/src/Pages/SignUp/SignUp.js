import React from "react";
import { Card } from "../../Components/shared/formElements/Card";
import { Input } from "../../Components/shared/formElements/Input";
import { Label } from "../../Components/shared/formElements/Label";
import { Button } from "../../Components/Button";

export const SignUpPage = () => {
  return (
    <div className="flex justify-center items-center h-screen bg-gradient-to-br from-blue-100 to-indigo-200">
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
        >
          Sign up
        </Button>
      </Card>
    </div>
  );
};
