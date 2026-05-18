
import { useState } from "react";

import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login({ setIsLoggedIn }) {

  const [email, setEmail] = useState("");

  const [password, setPassword] =
    useState("");
    const navigate = useNavigate();

  const handleLogin = async () => {

    try {

      if (!email || !password) {

        alert("Please fill all fields");

        return;
      }

      const response = await axios.post(
        "https://YOUR-RENDER-URL.onrender.com/api/login",
        {
          email,
          password,
        }
      );

      alert(response.data.message);

      setIsLoggedIn(true);
      navigate("/");
      localStorage.setItem(
  "user",
  JSON.stringify(
    response.data.user
  )
);
      localStorage.setItem(
  "isLoggedIn",
  "true"
);

    } catch (error) {

      console.error(error);

      alert(
        error.response?.data?.error ||
        "Login Failed"
      );

    }
  };

  return (

    <div className="flex items-center justify-center min-h-screen">

      <div className="bg-white p-10 rounded-2xl shadow w-full max-w-md">

        <h1 className="text-3xl font-bold mb-6 text-center text-black">

          Login

        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
          className="w-full border p-4 rounded-xl mb-4 text-black"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          className="w-full border p-4 rounded-xl mb-6 text-black"
        />

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white py-3 rounded-xl"
        >

          Login

        </button>

      </div>

    </div>

  );
}

export default Login;