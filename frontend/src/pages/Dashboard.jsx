import { useEffect, useState } from "react";

import axios from "axios";

function Dashboard() {

  const [favoritesCount, setFavoritesCount] =
    useState(0);

  const [analysisCount, setAnalysisCount] =
    useState(12);

  const [searchCount, setSearchCount] =
    useState(0);

  useEffect(() => {

    fetchFavorites();

    fetchSearchCount();

  }, []);

  const fetchFavorites = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:5001/api/favorites"
      );

      setFavoritesCount(
        response.data.length
      );

    } catch (error) {

      console.error(error);

    }
  };

  const fetchSearchCount = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:5001/api/analytics/search"
      );

      setSearchCount(
        response.data.count
      );

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <div>

      <h1 className="text-4xl font-bold mb-10">

        Dashboard

      </h1>

      {/* Analytics Cards */}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

        <div className="bg-blue-600 text-white rounded-2xl p-8 shadow">

          <h2 className="text-2xl font-bold mb-2">

            Favorites

          </h2>

          <p className="text-5xl font-bold">

            {favoritesCount}

          </p>

        </div>

        <div className="bg-green-600 text-white rounded-2xl p-8 shadow">

          <h2 className="text-2xl font-bold mb-2">

            Analyses

          </h2>

          <p className="text-5xl font-bold">

            {analysisCount}

          </p>

        </div>

        <div className="bg-purple-600 text-white rounded-2xl p-8 shadow">

          <h2 className="text-2xl font-bold mb-2">

            Searches

          </h2>

          <p className="text-5xl font-bold">

            {searchCount}

          </p>

        </div>

      </div>

      {/* Welcome Section */}

      <div className="bg-gray-900 text-white rounded-2xl shadow p-8">

        <h2 className="text-3xl font-bold mb-4">

          Welcome to Medical Research AI

        </h2>

        <p className="text-gray-300 text-lg">

          Analyze medical research papers,
          search scientific publications,
          save favorites, and generate
          AI-powered insights.

        </p>

      </div>

    </div>

  );
}

export default Dashboard;