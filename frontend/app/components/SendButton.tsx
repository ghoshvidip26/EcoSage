"use client";
import { FaArrowUp } from "react-icons/fa";

const SendButton = () => {
  return (
    <button
      type="submit"
      aria-label="Send message"
      className="group relative w-10 h-10 flex items-center justify-center rounded-full 
                 border-2 border-indigo-500/40 bg-indigo-600 
                 text-white shadow-md shadow-indigo-500/30 
                 hover:scale-110 hover:bg-indigo-700 hover:shadow-indigo-500/50 
                 active:scale-95 focus:outline-none focus:ring-2 focus:ring-indigo-400 
                 transition-all duration-300"
    >
      <FaArrowUp className="w-4 h-4 transition-transform duration-300 group-hover:-translate-y-0.5" />
    </button>
  );
};

export default SendButton;
