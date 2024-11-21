import React from "react";
import { Navbar } from "../Navbar/Navbar";
import { TaskList } from "../../Components/TaskList";
import { useState } from "react";
import { Footer } from "../../Components/Footer";
const initialTasks = [
  {
    id: 1,
    day: "Monday",
    title: "Complete project proposal",
    comments: [
      { id: 1, text: "Don't forget to include the budget breakdown" },
      { id: 2, text: "Add timeline for milestones" },
    ],
  },
  { id: 2, day: "Monday", title: "Team meeting", comments: [] },
  {
    id: 3,
    day: "Tuesday",
    title: "Review code",
    comments: [{ id: 3, text: "Focus on the new authentication module" }],
  },
  {
    id: 4,
    day: "Wednesday",
    title: "Client call",
    comments: [
      { id: 4, text: "Prepare demo of the latest features" },
      { id: 5, text: "Discuss next sprint priorities" },
      { id: 6, text: "Address any concerns from last meeting" },
    ],
  },
  { id: 5, day: "Thursday", title: "Write documentation", comments: [] },
  {
    id: 6,
    day: "Friday",
    title: "Submit report",
    comments: [{ id: 7, text: "Include all project updates from this week" }],
  },
];

export const days = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];
export const Tasks = () => {
  const [tasks, setTasks] = useState(initialTasks);
  const [selectedTask, setSelectedTask] = useState(null);
  const handleAddTask = (newTask) => {
    setTasks([...tasks, newTask]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-indigo-200 dark:from-gray-900 dark:to-gray-800 scroll-m-2">
      <Navbar />
      <TaskList
        tasks={tasks}
        onAddTask={handleAddTask}
        onSelectTask={setSelectedTask}
      />
      <Footer />
    </div>
  );
};
