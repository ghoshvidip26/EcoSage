import { RiRobot3Line } from "react-icons/ri";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";

interface BotMessageProps {
  botMessage: string;
}

const BotMessage = ({ botMessage }: BotMessageProps) => {
  const date = new Date();

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex w-full my-3 items-start gap-3"
    >
      <div className="flex justify-center items-center w-8 h-8 bg-[#19c37d] rounded-sm">
        <RiRobot3Line size={20} className="text-white" />
      </div>
      <motion.div
        initial={{ scale: 0.95 }}
        animate={{ scale: 1 }}
        className="inline-block rounded-lg bg-[#444654] p-4 text-lg text-gray-100 max-w-[75%] break-words shadow-sm"
      >
        <div className="prose prose-invert">
          <ReactMarkdown>{botMessage}</ReactMarkdown>
        </div>
        <div className="text-right mt-2">
          <span className="text-xs text-white/80">
            {date.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default BotMessage;
