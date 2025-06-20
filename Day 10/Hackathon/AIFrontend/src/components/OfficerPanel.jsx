import React from "react";

const OfficerPanel = ({ flaggedOffers }) => {
  return (
    <div className="max-w-3xl mx-auto mt-10">
      <h2 className="text-2xl font-bold text-red-600 mb-4">Flagged Offers</h2>
      <ul className="space-y-4">
        {flaggedOffers.map((offer, idx) => (
          <li key={idx} className="bg-red-50 border border-red-200 p-4 rounded">
            <div className="font-semibold">{offer.candidate}</div>
            <div>Probability: {offer.probability}%</div>
            <div className="text-sm text-gray-600">Action: {offer.suggestedAction}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OfficerPanel;
