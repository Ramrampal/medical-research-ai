import { useState } from "react";

function Chat() {

  const [message, setMessage] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const sendMessage = () => {

    if (!message) return;

    const userMessage = {

      type: "user",

      text: message,

    };

    const botMessage = {

      type: "bot",

      text:
        "AI Assistant suggests exploring recent clinical studies and evidence-based medical publications related to your query.",

    };

    setMessages([
      ...messages,
      userMessage,
      botMessage,
    ]);

    setMessage("");

  };

  return (

    <div>

      <h1 className="text-4xl font-bold mb-8">

        AI Research Assistant

      </h1>

      {/* Chat Area */}

      <div className="bg-white rounded-2xl shadow p-6 h-[500px] overflow-y-auto mb-6">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={
              msg.type === "user"
                ? "text-right mb-4"
                : "text-left mb-4"
            }
          >

            <div
              className={
                msg.type === "user"
                  ? "inline-block bg-blue-600 text-white px-4 py-3 rounded-2xl"
                  : "inline-block bg-gray-200 text-black px-4 py-3 rounded-2xl"
              }
            >

              {msg.text}

            </div>

          </div>

        ))}

      </div>

      {/* Input */}

      <div className="flex gap-4">

        <input
          type="text"
          placeholder="Ask medical AI..."
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          className="flex-1 border rounded-xl p-4 text-black"
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-6 rounded-xl"
        >

          Send

        </button>

      </div>

    </div>

  );
}

export default Chat;