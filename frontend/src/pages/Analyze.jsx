import { useState } from "react";

import axios from "axios";

import jsPDF from "jspdf";

function Analyze() {

  const [text, setText] = useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const analyzeResearch = async () => {

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5001/api/analyze",
        {
          text,
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert("API Error");

    } finally {

      setLoading(false);

    }
  };

  const downloadPDF = () => {

    if (!result) {

      alert("No analysis available");

      return;
    }

    const doc = new jsPDF();

    doc.setFontSize(20);

    doc.text(
      "Medical Research AI Report",
      20,
      20
    );

    doc.setFontSize(12);

    doc.text(
      `Accuracy: ${result.analysis.data_quality.accuracy}`,
      20,
      40
    );

    doc.text(
      `Completeness: ${result.analysis.data_quality.completeness}`,
      20,
      50
    );

    doc.text(
      `Consistency: ${result.analysis.data_quality.consistency}`,
      20,
      60
    );

    doc.text(
      `Overall Quality: ${result.analysis.data_quality.overall_quality}`,
      20,
      70
    );

    doc.save("research-report.pdf");
  };

  return (

    <div>

      <h1 className="text-4xl font-bold mb-6">

        Analyze Research

      </h1>

      <textarea
        className="w-full border border-gray-300 rounded-xl p-4 h-40 text-black"
        placeholder="Enter medical research text..."
        value={text}
        onChange={(e) =>
          setText(e.target.value)
        }
      />

      <button
        onClick={analyzeResearch}
        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold"
      >

        {loading
          ? "Analyzing..."
          : "Analyze Research"}

      </button>

      {result && (

        <div className="mt-8">

          <h2 className="text-2xl font-bold mb-6">

            Analysis Result

          </h2>

          <button
            onClick={downloadPDF}
            className="bg-green-600 text-white px-6 py-3 rounded-xl mb-6"
          >

            Download PDF

          </button>

          {/* Data Quality */}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">

            <div className="bg-blue-100 p-4 rounded-xl shadow">

              <h3 className="font-bold text-black">

                Accuracy

              </h3>

              <p className="text-2xl text-black">

                {result.analysis.data_quality.accuracy}

              </p>

            </div>

            <div className="bg-green-100 p-4 rounded-xl shadow">

              <h3 className="font-bold text-black">

                Completeness

              </h3>

              <p className="text-2xl text-black">

                {result.analysis.data_quality.completeness}

              </p>

            </div>

            <div className="bg-yellow-100 p-4 rounded-xl shadow">

              <h3 className="font-bold text-black">

                Consistency

              </h3>

              <p className="text-2xl text-black">

                {result.analysis.data_quality.consistency}

              </p>

            </div>

            <div className="bg-purple-100 p-4 rounded-xl shadow">

              <h3 className="font-bold text-black">

                Overall

              </h3>

              <p className="text-2xl text-black">

                {result.analysis.data_quality.overall_quality}

              </p>

            </div>

          </div>

          {/* Insights */}

          <div className="bg-white border rounded-xl p-6 shadow mb-6">

            <h3 className="text-xl font-bold mb-4 text-black">

              Key Insights

            </h3>

            {result.analysis.key_insights.map(
              (item, index) => (

              <div
                key={index}
                className="border-b py-3"
              >

                <p className="font-semibold text-black">

                  {item.insight}

                </p>

                <p className="text-sm text-gray-500">

                  Confidence:
                  {" "}
                  {item.confidence}

                </p>

              </div>

            ))}

          </div>

          {/* Recommendations */}

          <div className="bg-white border rounded-xl p-6 shadow">

            <h3 className="text-xl font-bold mb-4 text-black">

              Recommendations

            </h3>

            <ul className="list-disc pl-6 text-black">

              {result.analysis.recommendations.map(
                (rec, index) => (

                <li
                  key={index}
                  className="mb-2"
                >

                  {rec}

                </li>

              ))}

            </ul>

          </div>

        </div>

      )}

    </div>

  );
}

export default Analyze;