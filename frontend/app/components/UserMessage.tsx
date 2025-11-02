/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FiEdit2, FiCheck, FiX } from "react-icons/fi";
import { CiUser } from "react-icons/ci";

interface UserMessageProps {
  message: {
    id: string;
    text: string;
    imageUrl?: string;
    isEditing?: boolean;
  };
  onEdit?: (id: string) => void;
  onSaveEdit?: (id: string, newText: string) => void;
}

const UserMessage = ({ message, onEdit, onSaveEdit }: UserMessageProps) => {
  const [editText, setEditText] = useState(message.text);
  const [displayText, setDisplayText] = useState(message.text);
  const date = new Date();

  useEffect(() => {
    if (displayText !== message.text) {
      setDisplayText(message.text);
    }
  }, [displayText, message.text]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex w-full my-3 items-start justify-end gap-3"
    >
      {/* Message Bubble */}
      <motion.div
        initial={{ scale: 0.98 }}
        animate={{ scale: 1 }}
        className="relative bg-gradient-to-r from-indigo-500/60 to-blue-500/40 backdrop-blur-md border border-white/10 p-4 rounded-2xl text-white shadow-md max-w-[75%] transition-all duration-300 hover:shadow-lg hover:from-indigo-500/70"
      >
        {message.imageUrl && (
          <div className="mb-3">
            <img
              src={message.imageUrl}
              alt="Uploaded"
              className="max-w-full rounded-xl shadow-md"
            />
          </div>
        )}

        {message.isEditing ? (
          <div className="flex flex-col gap-2">
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              className="w-full p-2 bg-white/10 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300"
              rows={3}
              autoFocus
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => {
                  setDisplayText(editText);
                  onSaveEdit?.(message.id, editText);
                }}
                className="p-2 bg-green-500 rounded-lg hover:bg-green-600 transition-colors"
              >
                <FiCheck size={16} />
              </button>
              <button
                onClick={() => onEdit?.(message.id)}
                className="p-2 bg-red-500 rounded-lg hover:bg-red-600 transition-colors"
              >
                <FiX size={16} />
              </button>
            </div>
          </div>
        ) : (
          <>
            <p className="whitespace-pre-wrap text-[1.05rem] leading-relaxed">
              {displayText}
            </p>
            <button
              onClick={() => onEdit?.(message.id)}
              className="absolute top-2 right-2 p-1.5 bg-white/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white/20"
            >
              <FiEdit2 size={14} />
            </button>
          </>
        )}

        <div className="text-right mt-2">
          <span className="text-xs text-white/70">
            {date.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>
      </motion.div>

      {/* User Icon */}
      <div className="flex justify-center items-center w-10 h-10 bg-gradient-to-br from-indigo-600 to-blue-600 rounded-full shadow-lg">
        <CiUser size={22} className="text-white" />
      </div>
    </motion.div>
  );
};

export default UserMessage;
