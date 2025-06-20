import React from "react";

const CandidateAnalysisResult = ({data}) => {
  const {
    candidate_id,
    offer_analysis,
    preference_alignment,
    acceptance_prediction,
    upskill_recommendations,
    status,
  } = data;

  console.log('data: ', data);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-2xl shadow-xl space-y-8">
      <h1 className="text-2xl font-bold text-gray-800">Candidate Analysis Summary</h1>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">🆔 Candidate ID:</h2>
        <p className="text-gray-700">{candidate_id}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <section className="bg-gray-50 p-4 rounded-xl shadow">
          <h3 className="font-bold text-lg text-indigo-600 mb-2">📄 Offer Analysis</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li><strong>Position:</strong> {offer_analysis?.position || ""}</li>
            <li><strong>Salary:</strong> {offer_analysis?.salary}</li>
            <li><strong>Location:</strong> {offer_analysis?.location}</li>
            <li><strong>Start Date:</strong> {offer_analysis?.startDate}</li>
            <li><strong>Benefits:</strong> {offer_analysis?.benefits.join(", ") || "N/A"}</li>
          </ul>
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow">
          <h3 className="font-bold text-lg text-green-600 mb-2">🎯 Candidate Preferences</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li><strong>Preferred Salary:</strong> {preference_alignment?.preferredSalary}</li>
            <li><strong>Location Preference:</strong> {preference_alignment?.locationPreference}</li>
            <li><strong>Key Skills:</strong> {preference_alignment?.keySkills.join(", ")}</li>
            <li><strong>Alignment Score:</strong> {preference_alignment?.alignmentScore} / 100</li>
          </ul>
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow col-span-2">
          <h3 className="font-bold text-lg text-blue-600 mb-2">📈 Acceptance Prediction</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li><strong>Probability:</strong> {acceptance_prediction?.probability}%</li>
            <li><strong>Confidence:</strong> {acceptance_prediction?.confidence}%</li>
            <li><strong>Positive Factors:</strong> {acceptance_prediction?.positiveFactors.join(", ") || "N/A"}</li>
            <li><strong>Risk Factors:</strong> {acceptance_prediction?.riskFactors.join(", ") || "None"}</li>
          </ul>
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow col-span-2">
          <h3 className="font-bold text-lg text-yellow-600 mb-2">📚 Upskill Recommendations</h3>
          {upskill_recommendations?.recommendations?.length === 0 ? (
            <p className="text-sm text-gray-500 italic">No recommendations found.</p>
          ) : (
            <ul className="text-sm text-gray-700 list-disc list-inside space-y-1">
              {upskill_recommendations?.recommendations?.map((rec, index) => (
                <li key={index}>
                  <span className="font-semibold">{rec.goal}</span> – {rec.description}
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      <div className="mt-6 text-right">
        <span className={`px-4 py-2 rounded-full text-white text-sm font-semibold ${status === "pending" ? "bg-yellow-500" : "bg-green-500"}`}>
          Status: {status?.toUpperCase()}
        </span>
      </div>
    </div>
  );
};

export default CandidateAnalysisResult;
