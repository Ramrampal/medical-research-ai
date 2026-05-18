import { useState } from "react";

import axios from "axios";

function Signup() {

  const [name, setName] = useState("");

  const [email, setEmail] = useState("");

  const [password, setPassword] =
    useState("");

  const handleSignup = async () => {

    try {

      if (
        !name ||
        !email ||
        !password
      ) {

        alert("Please fill all fields");

        return;
      }

      const response = await axios.post(
        "https://medical-research-ai-production.up.railway.app/api/signup",
        {
          name,
          email,
          password,
        }
      );

      alert(response.data.message);

    } catch (error) {

      console.error(error);

      alert(
        error.response?.data?.error ||
        "Signup Failed"
      );

    }
  };

  return (

    <div className="flex items-center justify-center min-h-screen">

      <div className="bg-white p-10 rounded-2xl shadow w-full max-w-md">

        <h1 className="text-3xl font-bold mb-6 text-center text-black">

          Signup

        </h1>

        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) =>
            setName(e.target.value)
          }
          className="w-full border p-4 rounded-xl mb-4 text-black"
        />

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
          onClick={handleSignup}
          className="w-full bg-green-600 text-white py-3 rounded-xl"
        >

          Signup

        </button>

      </div>

    </div>

  );
}

export default Signup;