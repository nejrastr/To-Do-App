import React from "react";
//import { MessageCircle } from "react-lucide";

export const TaskItem = ({ onClick, task }) => {
  return (
    <div
      onClick={onClick}
      className="bg-gray-50 p-3 cursor-pointer hover:bg-gray-100 mb-2 rounded"
    >
      <p className="font-medium">{task.title}</p>
      <div>
        <span className="overflow-hidden">{task.comments.length} comments</span>
      </div>
    </div>
  );
};
