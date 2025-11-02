import axios from "axios";

export const handleResponse = async (
  message: string,
  imageUrl?: string
): Promise<string> => {
  try {
    const res = await axios.post(
      "/api/chat",
      { message, imageUrl },
      { headers: { "Content-Type": "application/json" } }
    );
    console.log("API Response:", res.data);
    const data = res.data;

    if (data?.message) {
      return data.message;
    } else if (data?.error) {
      throw new Error(data.error);
    }

    throw new Error("Unexpected response format");
  } catch (err: any) {
    console.error("handleResponse error:", err.message);
    return "⚠️ Server error. Please try again.";
  }
};
