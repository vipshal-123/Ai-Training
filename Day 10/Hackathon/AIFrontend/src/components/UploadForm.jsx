import React, { useState } from "react";
// import axios from "../services/api";

const UploadForm = () => {
  const [offerFile, setOfferFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("offer", offerFile);
    formData.append("resume", resumeFile);
    try {
    //   await axios.post("/upload", formData);
      alert("Upload successful");
    } catch (err) {
        console.log('err: ', err);
      alert("Upload failed");
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow-md mt-8">
      <h3 className="text-xl font-semibold mb-4 text-gray-700">Upload Documents</h3>
      <div className="space-y-4">
        <input type="file" onChange={(e) => setOfferFile(e.target.files[0])} className="w-full" />
        <input type="file" onChange={(e) => setResumeFile(e.target.files[0])} className="w-full" />
        <button
          onClick={handleUpload}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Upload
        </button>
      </div>
    </div>
  );
};

export default UploadForm;
