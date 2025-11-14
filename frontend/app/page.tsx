"use client";
import { motion } from "framer-motion";
import { useState } from "react";
import { Brain, Leaf, Sprout } from "lucide-react";
import SendButton from "./components/SendButton";
import Upload from "./components/Upload";
import { handleResponse } from "./utils/utils";

const agents = [
  {
    id: "llm",
    name: "LLM Assistant",
    icon: <Brain size={28} />,
    color: "from-purple-500 to-indigo-600",
    desc: "Ask general questions, get explanations, or reasoning support.",
  },
  {
    id: "crop",
    name: "Crop Advisor",
    icon: <Sprout size={28} />,
    color: "from-green-500 to-emerald-600",
    desc: "Get personalized crop recommendations using soil & environment data.",
  },
  {
    id: "disease",
    name: "Plant Doctor",
    icon: <Leaf size={28} />,
    color: "from-yellow-500 to-orange-600",
    desc: "Upload a leaf image to detect plant diseases instantly.",
  },
];

export default function MultiAgentPage() {
  const [selected, setSelected] = useState<string | null>(null);
  interface Message {
    sender: string;
    text: string;
    id?: string;
  }
  
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMessage = input;
    setMessages(prev => [...prev, { sender: "user", text: userMessage }]);
    setInput("");
    
    try {
      // Add a temporary loading message
      const loadingId = Date.now().toString();
      setMessages(prev => [...prev, { sender: "bot", text: "Thinking...", id: loadingId }]);
      
      // Get the response from the API
      const response = await handleResponse(userMessage, "");
      
      // Update the loading message with the actual response
      setMessages(prev => 
        prev.map(msg => 
          msg.id === loadingId 
            ? { ...msg, text: response, id: undefined } 
            : msg
        )
      );
    } catch (error) {
      console.error("Error in handleSend:", error);
      setMessages(prev => [...prev, { 
        sender: "bot", 
        text: "Sorry, I encountered an error. Please try again." 
      }]);
    }
  };

  return (
    <div className="min-h-screen bg-[#0e0f13] text-white flex flex-col items-center justify-center px-6">
      {!selected ? (
        <>
          <motion.h1
            initial={{ opacity: 0, y: -30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-5xl font-extrabold mb-12 text-transparent bg-clip-text bg-linear-to-r from-indigo-400 to-pink-500"
          >
            Choose Your AI Agent
          </motion.h1>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl">
            {agents.map((agent) => (
              <motion.div
                key={agent.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelected(agent.id)}
                className={`cursor-pointer bg-linear-to-br ${agent.color} p-1 rounded-2xl shadow-xl`}
              >
                <div className="bg-[#1e1f25] rounded-2xl h-full p-8 flex flex-col items-center text-center">
                  <div className="mb-4">{agent.icon}</div>
                  <h2 className="text-2xl font-semibold mb-2">{agent.name}</h2>
                  <p className="text-gray-400 text-sm">{agent.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </>
      ) : (
        <motion.div
          key={selected}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="w-full max-w-3xl h-[80vh] flex flex-col bg-[#1e1f25] rounded-2xl shadow-2xl p-6"
        >
          <button
            onClick={() => setSelected(null)}
            className="text-gray-400 hover:text-gray-200 mb-4"
          >
            ← Back to Agents
          </button>

          <div className="flex items-center gap-3 mb-4">
            {agents.find((a) => a.id === selected)?.icon}
            <h2 className="text-2xl font-semibold">
              {agents.find((a) => a.id === selected)?.name}
            </h2>
          </div>

          {/* Chat Section */}
          <div className="flex-1 overflow-y-auto bg-[#141518] rounded-xl p-4 space-y-4 mb-4">
            {messages.length === 0 ? (
              <p className="text-gray-500 text-center mt-20">
                Start chatting with the{" "}
                {agents.find((a) => a.id === selected)?.name} 👋
              </p>
            ) : (
              messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${
                    msg.sender === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`px-4 py-2 rounded-xl max-w-[75%] text-sm whitespace-pre-line ${
                      msg.sender === "user"
                        ? "bg-indigo-600 text-white"
                        : "bg-gray-700 text-gray-100"
                    }`}
                    dangerouslySetInnerHTML={{
                      __html: msg.text
                        .replace(/\n/g, '<br />')
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    }}
                  />
                </div>
              ))
            )}
          </div>

          {/* Input Section */}
          <form onSubmit={handleSend} className="flex items-center gap-3">
            {selected === "disease" && (
              <Upload onImageUpload={(url) => console.log("Uploaded:", url)} />
            )}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 bg-[#2b2c34] text-white rounded-xl px-4 py-3 text-sm focus:outline-none border border-gray-700"
            />
            <SendButton />
          </form>
        </motion.div>
      )}
    </div>
  );
}
