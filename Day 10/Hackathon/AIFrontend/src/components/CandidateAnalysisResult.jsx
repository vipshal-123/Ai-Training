import React, { useState } from "react";

const CandidateAnalysisResult = ({ data }) => {
  const {
    candidate_id,
    offer_analysis,
    preference_alignment,
    acceptance_prediction,
    upskill_recommendations,
    status,
    report,
  } = data;

  console.log("data: ", data);

  const [showModal, setShowModal] = useState(false);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-2xl shadow-xl space-y-8">
      <h1 className="text-2xl font-bold text-gray-800">
        Candidate Analysis Summary
      </h1>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">🆔 Candidate ID:</h2>
        <p className="text-gray-700">{candidate_id}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <section className="bg-gray-50 p-4 rounded-xl shadow">
          <h3 className="font-bold text-lg text-indigo-600 mb-2">
            📄 Offer Analysis
          </h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>
              <strong>Position:</strong> {offer_analysis?.position || ""}
            </li>
            <li>
              <strong>Salary:</strong> {offer_analysis?.salary}
            </li>
            <li>
              <strong>Location:</strong> {offer_analysis?.location}
            </li>
            <li>
              <strong>Start Date:</strong> {offer_analysis?.startDate}
            </li>
            <li>
              <strong>Benefits:</strong>{" "}
              {offer_analysis?.benefits.join(", ") || "N/A"}
            </li>
          </ul>
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow">
          <h3 className="font-bold text-lg text-green-600 mb-2">
            🎯 Candidate Preferences
          </h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>
              <strong>Preferred Salary:</strong>{" "}
              {preference_alignment?.preferredSalary}
            </li>
            <li>
              <strong>Location Preference:</strong>{" "}
              {preference_alignment?.locationPreference}
            </li>
            <li>
              <strong>Key Skills:</strong>{" "}
              {preference_alignment?.keySkills.join(", ")}
            </li>
            <li>
              <strong>Alignment Score:</strong>{" "}
              {preference_alignment?.alignmentScore} / 100
            </li>
          </ul>
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow col-span-2">
          <h3 className="font-bold text-lg text-blue-600 mb-2">
            📈 Acceptance Prediction
          </h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>
              <strong>Probability:</strong> {acceptance_prediction?.probability}
              %
            </li>
            <li>
              <strong>Confidence:</strong> {acceptance_prediction?.confidence}%
            </li>
            <li>
              <strong>Positive Factors:</strong>{" "}
              {acceptance_prediction?.positiveFactors.join(", ") || "N/A"}
            </li>
            <li>
              <strong>Risk Factors:</strong>{" "}
              {acceptance_prediction?.riskFactors.join(", ") || "None"}
            </li>
          </ul>
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow col-span-2">
          <h3 className="font-bold text-lg text-yellow-600 mb-2">
            📚 Upskill Recommendations
          </h3>
          {upskill_recommendations?.recommendations?.length === 0 ? (
            <p className="text-sm text-gray-500 italic">
              No recommendations found.
            </p>
          ) : (
            <ul className="text-sm text-gray-700 list-disc list-inside space-y-1">
              {upskill_recommendations?.recommendations?.map((rec, index) => (
                <li key={index}>
                  <span className="font-semibold">{rec.goal}</span> – {rec}
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="bg-gray-50 p-4 rounded-xl shadow col-span-2">
          <h3 className="font-bold text-lg text-yellow-600 mb-2">
            📚 Onboarding Resources
          </h3>
          {upskill_recommendations?.onboardingResource?.length === 0 ? (
            <p className="text-sm text-gray-500 italic">
              No onboarding Resource found.
            </p>
          ) : (
            <ul className="text-sm text-gray-700 list-disc list-inside space-y-1">
              {upskill_recommendations?.onboardingResource?.map(
                (rec, index) => (
                  <li key={index}>
                    <span className="font-semibold">{rec.goal}</span> – {rec}
                  </li>
                )
              )}
            </ul>
          )}
        </section>
      </div>

      <div className="flex justify-between items-center mt-6">
        <span
          className={`px-4 py-2 rounded-full text-white text-sm font-semibold ${
            status === "pending" ? "bg-yellow-500" : "bg-green-500"
          }`}
        >
          Status: {status?.toUpperCase()}
        </span>

        {/* Final Report Button */}
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition"
        >
          📘 View Final Report
        </button>
      </div>

      {/* Final Report Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white max-w-2xl w-full p-6 rounded-2xl shadow-xl relative space-y-4 overflow-y-auto max-h-[90vh]">
            <button
              onClick={() => setShowModal(false)}
              className="absolute top-2 right-3 text-gray-500 hover:text-gray-800 text-2xl font-bold"
            >
              &times;
            </button>
            <h2 className="text-xl font-bold text-indigo-700 mb-2">
              📋 Final Candidate Report
            </h2>
            <pre className="text-gray-800 whitespace-pre-wrap">
              {report
                .replace(/(🔍|📄|🧑‍💼|📈|🎯|✅)/g, "\n$1")
                .replace(/ - /g, "\n- ")}
            </pre>
          </div>
        </div>
      )}

      <div className="mt-6 text-right">
        <span
          className={`px-4 py-2 rounded-full text-white text-sm font-semibold ${
            status === "pending" ? "bg-yellow-500" : "bg-green-500"
          }`}
        >
          Status: {status?.toUpperCase()}
        </span>
      </div>
    </div>
  );
};

export default CandidateAnalysisResult;
