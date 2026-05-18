import React from "react";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Analyze from "./pages/Analyze";
import Search from "./pages/Search";
import Predict from "./pages/Predict";
import Favorites from "./pages/Favorites";
import Chat from "./pages/Chat";

import Login from "./pages/Login";
import Signup from "./pages/Signup";

function App() {

  const [darkMode, setDarkMode] =
    React.useState(false);

const [isLoggedIn, setIsLoggedIn] =
  React.useState(
    localStorage.getItem("isLoggedIn")
      === "true"
  );

  return (

    <BrowserRouter>

     <div
  className={
    darkMode
      ? "flex bg-gray-900 text-white min-h-screen"
      : "flex bg-gray-100 text-black min-h-screen"
  }
>

        {/* Sidebar */}

        <div className="relative">

          <Sidebar />

          {/* Logout Button */}

          <button
           onClick={() => {

  setIsLoggedIn(false);

  localStorage.removeItem(
    "isLoggedIn"
  );
  localStorage.removeItem("user");

}}
            className="absolute bottom-24 left-10 bg-red-500 text-white px-4 py-2 rounded-xl shadow"
          >
            Logout
          </button>

          {/* Dark Mode Button */}

          <button
            onClick={() =>
              setDarkMode(!darkMode)
            }
            className="absolute bottom-10 left-10 bg-white text-black px-4 py-2 rounded-xl shadow"
          >
            {darkMode
              ? "Light Mode"
              : "Dark Mode"}
          </button>

        </div>

        {/* Main Content */}

       <div
  className={
    darkMode
      ? "flex-1 p-8 bg-gray-800 min-h-screen text-white transition-all duration-300"
      : "flex-1 p-8 bg-gray-100 min-h-screen text-black transition-all duration-300"
  }
>

          <Routes>

            <Route
              path="/"
              element={
                isLoggedIn
                  ? <Dashboard />
                  : (
                    <Login
                      setIsLoggedIn={
                        setIsLoggedIn
                      }
                    />
                  )
              }
            />

            <Route
              path="/analyze"
              element={<Analyze />}
            />

            <Route
              path="/search"
              element={<Search />}
            />

            <Route
              path="/predict"
              element={<Predict />}
            />
            <Route
  path="/favorites"
  element={<Favorites />}
/>
<Route
  path="/chat"
  element={<Chat />}
 />

            <Route
              path="/login"
              element={
                <Login
                  setIsLoggedIn={
                    setIsLoggedIn
                  }
                />
              }
            />

            <Route
              path="/signup"
              element={<Signup />}
            />

          </Routes>

        </div>

      </div>

    </BrowserRouter>

  );
}

export default App;