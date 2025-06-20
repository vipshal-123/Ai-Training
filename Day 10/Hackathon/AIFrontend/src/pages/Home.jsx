import React, { useState, useRef } from "react";
import {
  Upload,
  FileText,
  User,
  Brain,
  BookOpen,
  BarChart3,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Download,
  Eye,
  Trash2,
  Plus,
  RefreshCw,
  TrendingUp,
  Users,
  Clock,
  Target,
} from "lucide-react";
import { details, uploadFile } from "../services/auth.service";
import CandidateAnalysisResult from "../components/CandidateAnalysisResult";

const Home = () => {
  const [activeTab, setActiveTab] = useState("upload");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const fileInputRef = useRef(null);
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  console.log("data: ", data);

  // Mock data for demonstration
  const mockResults = {
    offerAnalysis: {
      position: "Senior Software Engineer",
      salary: "$95,000",
      location: "San Francisco, CA",
      benefits: ["Health Insurance", "401k", "Remote Work"],
      startDate: "2024-01-15",
    },
    candidatePreference: {
      alignmentScore: 85,
      preferredSalary: "$90,000 - $100,000",
      locationPreference: "Remote/Hybrid",
      keySkills: ["React", "Node.js", "Python", "AWS"],
    },
    acceptanceLikelihood: {
      probability: 78,
      confidence: 92,
      riskFactors: ["Salary slightly below market rate", "Location mismatch"],
      positiveFactors: ["Strong skill alignment", "Good benefits package"],
    },
    upskillRecommendations: [
      { skill: "Advanced React", priority: "High", resources: 3 },
      { skill: "System Design", priority: "Medium", resources: 5 },
      { skill: "Leadership", priority: "Low", resources: 2 },
    ],
  };

  const mockCandidates = [
    {
      id: 1,
      name: "John Doe",
      position: "Frontend Developer",
      acceptanceProbability: 85,
      status: "pending",
      uploadDate: "2024-06-18",
      riskLevel: "low",
    },
    {
      id: 2,
      name: "Jane Smith",
      position: "Full Stack Engineer",
      acceptanceProbability: 45,
      status: "review",
      uploadDate: "2024-06-17",
      riskLevel: "high",
    },
    {
      id: 3,
      name: "Mike Johnson",
      position: "DevOps Engineer",
      acceptanceProbability: 92,
      status: "approved",
      uploadDate: "2024-06-16",
      riskLevel: "low",
    },
  ];

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    const newFiles = files.map((file) => ({
      id: Date.now() + Math.random(),
      name: file.name,
      size: file.size,
      type: file.type,
      file: file,
    }));
    setUploadedFiles((prev) => [...prev, ...newFiles]);
  };

  const removeFile = (fileId) => {
    setUploadedFiles((prev) => prev.filter((file) => file.id !== fileId));
  };

  //   const processFiles = async () => {
  //     setIsProcessing(true);
  //     // Simulate API processing
  //     setTimeout(() => {
  // setResults(mockResults);
  // setCandidates(mockCandidates);
  //       setIsProcessing(false);
  //       setActiveTab("results");
  //     }, 3000);
  //   };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const getRiskColor = (level) => {
    switch (level) {
      case "low":
        return "text-green-600 bg-green-100";
      case "medium":
        return "text-yellow-600 bg-yellow-100";
      case "high":
        return "text-red-600 bg-red-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "approved":
        return "text-green-600 bg-green-100";
      case "pending":
        return "text-blue-600 bg-blue-100";
      case "review":
        return "text-orange-600 bg-orange-100";
      case "rejected":
        return "text-red-600 bg-red-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const fetchData = async () => {
    try {
      const response = await details();
      if (response.success) {
        setData(response.data);
      }
    } catch (error) {
      console.error(error);
      alert("An error occurred while processing the files.");
    }
  };

  const changeTab = async (tab) => {
    setActiveTab(tab);
    if (tab === "results") {
      await fetchData();
    }
  };

  const processFiles = async () => {
    const resumeFile = uploadedFiles.find((f) =>
      f.name.toLowerCase().includes("resume")
    );
    const offerFile = uploadedFiles.find((f) =>
      f.name.toLowerCase().includes("offer")
    );

    if (!resumeFile || !offerFile) {
      alert("Please upload both a resume and an offer letter.");
      return;
    }

    const formData = new FormData();
    formData.append("candidate_id", `CAND_${Date.now()}`);
    formData.append("resume", resumeFile.file);
    formData.append("offer", offerFile.file);
    formData.append(
      "placement_data",
      "Prefers remote work, salary above 10 LPA, backend roles"
    );
    formData.append(
      "placement_history",
      "Rejected 2 offers due to bond and relocation"
    );

    try {
      setLoading(true);
      const response = await uploadFile(formData);

      const result = await response;
      console.log("✅ Result:", result);

      if (result.success) {
        alert("Files analyzed successfully!");
        setResults(mockResults);
        setCandidates(mockCandidates);
        setActiveTab("results"); // or dashboard
        await fetchData();
        setLoading(false);
      } else {
        setLoading(false);
        alert(result.message || "Analysis failed.");
      }
    } catch (err) {
      setLoading(false);
      console.error(err);
      alert("An error occurred while processing the files.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Offer Acceptance Predictor
              </h1>
              <p className="text-sm text-gray-600">
                AI-Powered Pre-Onboarding Enabler
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-blue-50 px-3 py-2 rounded-lg">
                <Users className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-900">
                  {candidates.length} Candidates
                </span>
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2">
                <Plus className="h-4 w-4" />
                <span>New Analysis</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg mb-8">
          {[
            { id: "upload", label: "Upload Files", icon: Upload },
            { id: "results", label: "Analysis Results", icon: BarChart3 },
            { id: "dashboard", label: "Dashboard", icon: TrendingUp },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => changeTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md font-medium transition-colors ${
                activeTab === tab.id
                  ? "bg-white text-blue-600 shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Upload Tab */}
        {activeTab === "upload" && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Upload Documents
              </h2>

              {/* File Upload Area */}
              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 cursor-pointer transition-colors"
              >
                <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-lg font-medium text-gray-900 mb-2">
                  Drop files here or click to upload
                </p>
                <p className="text-sm text-gray-600">
                  Support for PDF, DOCX files (Resumes & Offer Letters)
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".pdf,.docx,.doc"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>

              {/* Uploaded Files List */}
              {uploadedFiles.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Uploaded Files
                  </h3>
                  <div className="space-y-3">
                    {uploadedFiles.map((file) => (
                      <div
                        key={file.id}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                      >
                        <div className="flex items-center space-x-3">
                          <FileText className="h-8 w-8 text-blue-600" />
                          <div>
                            <p className="font-medium text-gray-900">
                              {file.name}
                            </p>
                            <p className="text-sm text-gray-600">
                              {formatFileSize(file.size)}
                            </p>
                          </div>
                        </div>
                        <button
                          onClick={() => removeFile(file.id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Process Button */}
              {uploadedFiles.length > 0 && (
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={processFiles}
                    disabled={isProcessing}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
                  >
                    {isProcessing ? (
                      <>
                        <RefreshCw className="h-4 w-4 animate-spin" />
                        <span>Processing...</span>
                      </>
                    ) : (
                      <>
                        <Brain className="h-4 w-4" />
                        {loading ? (
                          <span>Loading...</span>
                        ) : (
                          <span>Analyze Documents</span>
                        )}
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>

            {/* Processing Status */}
            {isProcessing && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Processing Status
                </h3>
                <div className="space-y-4">
                  {[
                    {
                      step: "Offer Analysis",
                      status: "completed",
                      time: "< 30s",
                    },
                    {
                      step: "Preference Assessment",
                      status: "processing",
                      time: "< 20s",
                    },
                    {
                      step: "Acceptance Prediction",
                      status: "pending",
                      time: "< 15s",
                    },
                    {
                      step: "Resource Retrieval",
                      status: "pending",
                      time: "< 30s",
                    },
                    {
                      step: "Dashboard Update",
                      status: "pending",
                      time: "< 10s",
                    },
                  ].map((item, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      {item.status === "completed" && (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      )}
                      {item.status === "processing" && (
                        <RefreshCw className="h-5 w-5 text-blue-600 animate-spin" />
                      )}
                      {item.status === "pending" && (
                        <Clock className="h-5 w-5 text-gray-400" />
                      )}
                      <span className="flex-1 font-medium text-gray-900">
                        {item.step}
                      </span>
                      <span className="text-sm text-gray-600">{item.time}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Results Tab */}
        {activeTab === "results" && data && (
          <>
            <CandidateAnalysisResult data={data} />
          </>
        )}

        {/* Dashboard Tab */}
        {activeTab === "dashboard" && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center space-x-3">
                  <Users className="h-8 w-8 text-blue-600" />
                  <div>
                    <p className="text-sm text-gray-600">Total Candidates</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {candidates.length}
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center space-x-3">
                  <TrendingUp className="h-8 w-8 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600">
                      Avg. Acceptance Rate
                    </p>
                    <p className="text-2xl font-bold text-gray-900">74%</p>
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="h-8 w-8 text-purple-600" />
                  <div>
                    <p className="text-sm text-gray-600">High Confidence</p>
                    <p className="text-2xl font-bold text-gray-900">2</p>
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="h-8 w-8 text-red-600" />
                  <div>
                    <p className="text-sm text-gray-600">High Risk</p>
                    <p className="text-2xl font-bold text-gray-900">1</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Candidates Table */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Candidate Analysis Dashboard
                </h2>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2">
                  <Download className="h-4 w-4" />
                  <span>Export Report</span>
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Candidate
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Position
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Acceptance Probability
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Risk Level
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Status
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Upload Date
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {candidates.map((candidate) => (
                      <tr
                        key={candidate.id}
                        className="border-b border-gray-100 hover:bg-gray-50"
                      >
                        <td className="py-4 px-4">
                          <div className="flex items-center space-x-3">
                            <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center">
                              <span className="text-white font-medium text-sm">
                                {candidate.name
                                  .split(" ")
                                  .map((n) => n[0])
                                  .join("")}
                              </span>
                            </div>
                            <span className="font-medium text-gray-900">
                              {candidate.name}
                            </span>
                          </div>
                        </td>
                        <td className="py-4 px-4 text-gray-600">
                          {candidate.position}
                        </td>
                        <td className="py-4 px-4">
                          <div className="flex items-center space-x-2">
                            <div className="flex-1 bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${
                                  candidate.acceptanceProbability >= 80
                                    ? "bg-green-600"
                                    : candidate.acceptanceProbability >= 60
                                    ? "bg-yellow-600"
                                    : "bg-red-600"
                                }`}
                                style={{
                                  width: `${candidate.acceptanceProbability}%`,
                                }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium text-gray-900">
                              {candidate.acceptanceProbability}%
                            </span>
                          </div>
                        </td>
                        <td className="py-4 px-4">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${getRiskColor(
                              candidate.riskLevel
                            )}`}
                          >
                            {candidate.riskLevel}
                          </span>
                        </td>
                        <td className="py-4 px-4">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${getStatusColor(
                              candidate.status
                            )}`}
                          >
                            {candidate.status}
                          </span>
                        </td>
                        <td className="py-4 px-4 text-gray-600">
                          {candidate.uploadDate}
                        </td>
                        <td className="py-4 px-4">
                          <div className="flex items-center space-x-2">
                            <button className="text-blue-600 hover:text-blue-800">
                              <Eye className="h-4 w-4" />
                            </button>
                            <button className="text-green-600 hover:text-green-800">
                              <Download className="h-4 w-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
