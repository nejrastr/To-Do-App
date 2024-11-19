import React from "react";
import { CheckCircle, Calendar, StarIcon } from "lucide-react";
import { Button } from "./Button";

export const Hero = () => {
  return (
    <div className="text-center space-y-6 max-w-screen-2xl">
      <h2 className="text-3xl font-extrabold text-primary sm:text-5xl md:text-6xl">
        Plan Your Day, Achieve Your Goals
      </h2>
      <p className="text-xl text-muted-foreground sm:text-2x1">
        Organize your tasks, goals and important events. Boost your
        productivity, and take control of your future.
      </p>
      <div className="flex justify-center space-x-5">
        <div className="flex items-center">
          <CheckCircle className="mr-2" />
          <span>Task Management</span>
        </div>
        <div className="flex items-center">
          <Calendar className="mr-2" />
          <span>Remember Important Events</span>
        </div>
        <div className="flex items-center">
          <StarIcon className="mr-2" />
          <span>Set your goals</span>
        </div>
      </div>
      <div className="m-3">
        <Button color="black" label="Start Planning Your Future"></Button>
      </div>
    </div>
  );
};
