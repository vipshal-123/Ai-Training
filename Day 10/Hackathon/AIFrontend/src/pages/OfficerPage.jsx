import React, { useEffect, useState } from "react";
import OfficerPanel from "../components/OfficerPanel";
// import axios from "../services/api";

const OfficerPage = () => {
  const [flaggedOffers, setFlaggedOffers] = useState([]);

//   useEffect(() => {
//     axios.get("/flagged-offers").then((res) => setFlaggedOffers(res.data));
//   }, []);

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-10">
      <h1 className="text-3xl font-bold text-center text-red-700 mb-6">
        Placement Officer Panel
      </h1>
      <OfficerPanel flaggedOffers={flaggedOffers} />
    </div>
  );
};

export default OfficerPage;
