"use client"
import axios from "axios";

export const handleResponse = async (
  message: string,
  imageUrl?: string
): Promise<string> => {
  try {
    console.log("Message: ", message);
    const res = await axios.post(
      "http://127.0.0.1:3000/recommend-crop",
      { user_input: message, imageUrl },
      { 
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        } 
      }
    );
    console.log("API Response:", res.data);
    const data = res.data;
    console.log("Data: ", data);
    if (data?.recommendation) {
      return data.recommendation;
    } else if (data?.error) {
      throw new Error(data.error);
    }

    throw new Error("Unexpected response format");
  } catch (err: any) {
    console.error("handleResponse error:", err.message);
    return "⚠️ Server error. Please try again.";
  }
};
