import React from "react";
import Dashboard from "../components/Dashboard";

const DashboardPage = () => {
  return (
    <div className="min-h-screen bg-gray-100 px-4 py-10">
      <h1 className="text-3xl font-bold text-center text-green-700 mb-6">
        Candidate Dashboard
      </h1>
      <Dashboard />
    </div>
  );
};

export default DashboardPage;
