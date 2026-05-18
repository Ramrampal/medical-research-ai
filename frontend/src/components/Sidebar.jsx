import { Link } from "react-router-dom";

function Sidebar() {

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  return (

    <div className="w-64 min-h-screen bg-gray-900 text-white p-6">

      {/* Logo / Title */}

      <h1 className="text-3xl font-bold mb-2">

        Medical AI

      </h1>

      {/* User Info */}

      <p className="text-sm text-gray-300 mb-10">

        Welcome,
        {" "}
        {user?.name || "User"}

      </p>

      {/* Navigation */}

      <ul className="space-y-6 text-lg">

        <li>

          <Link
            to="/"
            className="hover:text-blue-400"
          >
            Dashboard
          </Link>

        </li>

        <li>

          <Link
            to="/analyze"
            className="hover:text-blue-400"
          >
            Analyze
          </Link>

        </li>

        <li>

          <Link
            to="/search"
            className="hover:text-blue-400"
          >
            Search
          </Link>

        </li>

        <li>

          <Link
            to="/predict"
            className="hover:text-blue-400"
          >
            Predict
          </Link>

        </li>

        <li>

          <Link
            to="/favorites"
            className="hover:text-blue-400"
          >
            Favorites
          </Link>

        </li>
        <li>

  <Link
    to="/chat"
    className="hover:text-blue-400"
  >

    AI Chat

  </Link>

</li>

        <li>

          <Link
            to="/login"
            className="hover:text-blue-400"
          >
            Login
          </Link>

        </li>

        <li>

          <Link
            to="/signup"
            className="hover:text-blue-400"
          >
            Signup
          </Link>

        </li>

      </ul>

    </div>

  );
}

export default Sidebar;