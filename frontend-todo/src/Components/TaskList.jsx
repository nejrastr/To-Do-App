import React, { useState } from "react";
import { days } from "../Pages/Tasks/Tasks";
import { Input } from "./shared/formElements/Input";
import { TaskItem } from "./TaskItem";
import { Button } from "./Button";

export const TaskList = ({ tasks, onAddTask, onSelectTask }) => {
  const [newTaskDay, setNewTaskDay] = useState(null);
  const [taskTitle, setTaskTitle] = useState("task title");

  const handleAddTask = (e) => {
    e.preventDefault();

    const newTask = {
      id: Math.max(...tasks.map((t) => t.id)) + 1,
      day: newTaskDay,
      title: taskTitle,
      comments: [],
    };

    onAddTask(newTask);
    setNewTaskDay(null);
  };

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-7">
      {days.map((day) => (
        <div
          key={day}
          className="bg-white p-4 shadow mt-5 ml-2 mr-2 overflow-hidden"
        >
          <h2 className="text-xl font-semibold mb-4">{day}</h2>

          {tasks
            .filter((task) => task.day === day)
            .map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onClick={() => onSelectTask(task)}
              />
            ))}
          {newTaskDay === day ? (
            <form onSubmit={handleAddTask}>
              <Input
                placeholder="Add task here"
                onChange={(value) => {
                  setTaskTitle(value);
                }}
                className="w-full mb-2"
                required
              />
              <div className="flex space-x-3 mt-2">
                <Button type="submit" label="Add task" />
              </div>
            </form>
          ) : (
            <div className="flex space-x-3">
              <Button
                label="Add Task"
                onClick={() => {
                  setNewTaskDay(day);
                }}
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
