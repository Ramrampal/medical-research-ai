import { useEffect, useState } from "react";

import axios from "axios";

function Favorites() {

  const [favorites, setFavorites] =
    useState([]);

  useEffect(() => {

    fetchFavorites();

  }, []);

  const fetchFavorites = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:5001/api/favorites"
      );

      setFavorites(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <div>

      <h1 className="text-4xl font-bold mb-8">

        My Favorites

      </h1>

      <div className="space-y-6">

        {favorites.map((item, index) => (

          <div
            key={index}
            className="bg-white rounded-2xl shadow p-6"
          >

            <h2 className="text-2xl font-bold mb-3 text-black">

              {item.title}

            </h2>

            <p className="text-gray-600">

              {item.abstract ||
                "No abstract available"}

            </p>

          </div>

        ))}

      </div>

    </div>

  );
}

export default Favorites;