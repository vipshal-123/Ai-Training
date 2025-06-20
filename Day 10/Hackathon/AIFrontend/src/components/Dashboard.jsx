import React, { useEffect, useState } from "react";
// import axios from "../services/api";

const Dashboard = () => {
  const [predictions, setPredictions] = useState([]);

//   useEffect(() => {
//     axios.get("/dashboard").then((res) => setPredictions(res.data));
//   }, []);

  return (
    <div className="max-w-3xl mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Prediction Dashboard</h2>
      <ul className="space-y-4">
        {predictions.map((item, i) => (
          <li key={i} className="bg-white p-4 shadow rounded border border-gray-200">
            <div className="text-lg font-medium">{item.candidateName}</div>
            <div>Acceptance: <span className="font-bold text-blue-600">{item.probability}%</span></div>
            <div className="text-sm text-gray-500">Suggested Action: {item.action}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
