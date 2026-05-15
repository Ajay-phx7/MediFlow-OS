import { useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import { postDoctorScribe } from "../../api/index.js";

const AIScribe = () => {
  const [transcript, setTranscript] = useState(
    "Doctor: Can you describe the chest discomfort?\nPatient: It feels tight and comes and goes.\nDoctor: Any dizziness or shortness of breath?\nPatient: Mild shortness of breath during stairs."
  );
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    setIsLoading(true);
    const response = await postDoctorScribe({ transcript });
    setResult(response.data);
    setIsLoading(false);
  };

  const handleCopy = () => {
    if (!result?.notes) return;
    navigator.clipboard.writeText(result.notes);
  };

  return (
    <div className="space-y-8">
      <Navbar title="AI Scribe" subtitle="Consultation Assistant" />

      <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-4">
        <div>
          <p className="text-sm text-slate-500">Start consultation</p>
          <h3 className="text-lg font-semibold text-slate-900">Ravi Kumar</h3>
          <p className="text-sm text-slate-600">Chief complaint: Chest discomfort</p>
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700">Conversation transcript</label>
          <textarea
            className="mt-2 w-full min-h-[160px] border border-slate-200 rounded-xl p-3 text-sm"
            value={transcript}
            onChange={(event) => setTranscript(event.target.value)}
          />
        </div>

        <button
          className="px-4 py-2 rounded-xl bg-blue-600 text-white text-sm font-semibold"
          onClick={handleGenerate}
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Notes & Prescription"}
        </button>
      </div>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-slate-900">SOAP Notes</h3>
              <button
                className="text-xs font-semibold text-blue-600 hover:text-blue-700"
                onClick={handleCopy}
              >
                Copy
              </button>
            </div>
            <p className="text-sm text-slate-600 mt-3 whitespace-pre-line">{result.notes}</p>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-slate-900">Prescription</h3>
            <table className="w-full text-left text-sm mt-4">
              <thead className="text-slate-500">
                <tr>
                  <th className="py-2 font-medium">Medication</th>
                  <th className="py-2 font-medium">Dosage</th>
                  <th className="py-2 font-medium">Duration</th>
                </tr>
              </thead>
              <tbody>
                {result.prescription.map((item) => (
                  <tr key={item.medication} className="border-t border-slate-100">
                    <td className="py-2 text-slate-700">{item.medication}</td>
                    <td className="py-2 text-slate-700">{item.dosage}</td>
                    <td className="py-2 text-slate-700">{item.duration}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIScribe;
