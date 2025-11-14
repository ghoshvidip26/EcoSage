import { useState, useEffect } from "react";
import { FaUpload } from "react-icons/fa";
import { FiX, FiEdit2 } from "react-icons/fi";
import { motion } from "framer-motion";

interface UploadProps {
  onImageUpload?: (imageUrl: string) => void;
  onReset?: (resetFn: () => void) => void;
}

export default function Upload({ onImageUpload, onReset }: UploadProps) {
  const [imgUrl, setImgUrl] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadStagedFile = async (stagedFile: File | Blob) => {
    setUploading(true);
    setError(null);
    try {
      const form = new FormData();
      form.set("file", stagedFile);

      const uploadRes = await fetch("http://127.0.0.1:3001/agent", {
        method: "POST",
        body: form,
      });

      console.log("Upload res: ", uploadRes);

      if (!uploadRes.ok) {
        throw new Error("Upload failed");
      }

      const data = await uploadRes.json();
      console.log("Data: ", data);
      const imgURL = data.imgUrl;
      setImgUrl(imgURL);
      onImageUpload?.(imgURL);
    } catch (err) {
      console.error("Upload error:", err);
      setError("Upload failed. Please try again.");
      onImageUpload?.("");
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const previewURL = URL.createObjectURL(file);
      setPreview(previewURL);
      uploadStagedFile(file);
    }
  };

  const resetState = () => {
    setPreview(null);
    setImgUrl(null);
    setError(null);
    onImageUpload?.("");
  };

  useEffect(() => {
    if (onReset) {
      onReset(resetState);
    }
  }, []);

  return (
    <div className="flex items-center justify-center">
      {preview ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative w-28 h-28 rounded-xl overflow-hidden group shadow-lg border border-white/10 bg-white/5 backdrop-blur-md"
        >
          <img
            src={preview}
            alt="Preview"
            className={`object-cover w-full h-full transition-all duration-300 ${
              uploading ? "opacity-70 blur-sm" : "opacity-100"
            }`}
          />

          {/* Overlay when uploading */}
          {uploading && (
            <div className="absolute inset-0 bg-black/40 flex flex-col items-center justify-center text-sm text-white font-medium">
              <div className="w-5 h-5 border-2 border-white/60 border-t-transparent rounded-full animate-spin mb-2"></div>
              Uploading...
            </div>
          )}

          {/* Remove button */}
          <button
            onClick={resetState}
            aria-label="Remove image"
            className="absolute top-2 right-2 p-1.5 bg-black/40 backdrop-blur-md rounded-full text-white hover:bg-black/70 transition"
          >
            <FiX size={14} />
          </button>

          {/* Edit button (placeholder for future) */}
          <button
            aria-label="Edit image"
            className="absolute top-2 left-2 p-1.5 bg-black/40 backdrop-blur-md rounded-full text-white hover:bg-black/70 transition"
          >
            <FiEdit2 size={14} />
          </button>
        </motion.div>
      ) : (
        <label
          htmlFor="file-upload"
          className="flex items-center justify-center w-12 h-12 bg-white/10 hover:bg-white/20 border border-dashed border-gray-400 rounded-xl cursor-pointer transition-all shadow-sm hover:shadow-md"
        >
          <FaUpload className="text-white/70" />
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>
      )}

      {/* Upload error feedback */}
      {error && (
        <p className="ml-3 text-sm text-red-400 font-medium">{error}</p>
      )}
    </div>
  );
}
