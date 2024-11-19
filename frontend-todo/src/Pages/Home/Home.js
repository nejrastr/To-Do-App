import React from "react";
import { Header } from "../../Components/Header";
import { Hero } from "../../Components/Hero";
import { Footer } from "../../Components/Footer";

export const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-100 to-indigo-200 dark:from-gray-900 dark:to-gray-800">
      <Header />
      <main className="flex-grow flex items-center justify-center px-4">
        <Hero />
      </main>
      <Footer />
    </div>
  );
};
