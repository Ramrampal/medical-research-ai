import { useState } from "react";

import axios from "axios";

function Search() {

  const [query, setQuery] = useState("");

  const [results, setResults] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [selectedPaper, setSelectedPaper] =
    useState(null);

  const searchResearch = async () => {

    try {

      setLoading(true);

      const response = await axios.post(
        "https://medical-research-ai-production.up.railway.app/api/search/combined",
        {
          query,
        }
      );

      const searchResults =
        response?.data?.results?.openalex?.works || [];

      setResults(searchResults);

    } catch (error) {

      console.error(error);

      alert("Search API Error");

    } finally {

      setLoading(false);

    }
  };

  const saveFavorite = async (paper) => {

    try {

      await axios.post(
        "https://medical-research-ai-production.up.railway.app/api/favorites",
        {
          title:
            paper.title ||
            paper.display_name,

          abstract:
            paper.abstract ||
            "No abstract available",
        }
      );

      alert("Saved to Favorites");

    } catch (error) {

      console.error(error);

      alert("Save Failed");

    }
  };

  return (

    <div>

      <h1 className="text-4xl font-bold mb-6">

        Research Search

      </h1>

      {/* Search Box */}

      <div className="flex gap-4 mb-8">

        <input
          type="text"
          placeholder="Search medical research..."
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          className="flex-1 border border-gray-300 rounded-xl p-4"
        />

        <button
          onClick={searchResearch}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 rounded-xl"
        >

          {loading
            ? "Searching..."
            : "Search"}

        </button>

      </div>

      {/* Search Results */}

      <div className="space-y-6">

        {Array.isArray(results) &&
          results.map((item, index) => (

            <div
              key={index}
              className="bg-white rounded-2xl shadow p-6"
            >

              <h2 className="text-2xl font-bold mb-3 text-black">

                {item.title ||
                  item.display_name ||
                  "Research Paper"}

              </h2>

              <p className="text-gray-600 mb-4">

                {
                  item.abstract
                    ? item.abstract
                    : item.abstract_inverted_index
                    ? "Abstract available from OpenAlex"
                    : "No abstract available"
                }

              </p>

              <div className="flex justify-between items-center mt-4">

                <div className="text-sm text-gray-500">

                  Source:
                  {" "}
                  {item.source ||
                    "Medical Database"}

                </div>

                <div className="flex gap-3">

                  <button
                    onClick={() =>
                      saveFavorite(item)
                    }
                    className="bg-green-600 text-white px-4 py-2 rounded-xl"
                  >

                    Save

                  </button>

                  <button
                    onClick={() =>
                      setSelectedPaper(item)
                    }
                    className="bg-blue-600 text-white px-4 py-2 rounded-xl"
                  >

                    View Details

                  </button>

                </div>

              </div>

            </div>

        ))}

      </div>

      {/* Modal */}

      {selectedPaper && (

        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-6">

          <div className="bg-white rounded-2xl p-8 max-w-2xl w-full">

            <h2 className="text-3xl font-bold mb-4 text-black">

              {selectedPaper.title ||
                selectedPaper.display_name}

            </h2>

            <p className="text-gray-600 mb-4">

              {
                selectedPaper.abstract
                  ? selectedPaper.abstract
                  : "Abstract available from OpenAlex"
              }

            </p>

            <div className="mb-4 text-black">

              <p>

                <strong>Publication Year:</strong>
                {" "}
                {selectedPaper.publication_year ||
                  "N/A"}

              </p>

              <p>

                <strong>Citations:</strong>
                {" "}
                {selectedPaper.cited_by_count ||
                  "N/A"}

              </p>

            </div>

            <button
              onClick={() =>
                setSelectedPaper(null)
              }
              className="bg-red-500 text-white px-5 py-2 rounded-xl"
            >

              Close

            </button>

          </div>

        </div>

      )}

    </div>

  );
}

export default Search;