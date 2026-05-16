import { useState, useEffect, useContext } from "react";

import ChatPanel from "../../components/ChatPanel.jsx";
import Navbar from "../../components/Navbar.jsx";
import { AppContext } from "../../context/AppContext.jsx";
import { getAllChat, sendChatMessage } from "../../api/index.js";

const DeptChat = () => {
  const { selectedAdmin } = useContext(AppContext);
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Fetch all messages on mount and set up polling
  useEffect(() => {
    fetchMessages();
    // Set up polling to refresh messages every 3 seconds
    const interval = setInterval(fetchMessages, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await getAllChat();
      if (response.data.messages) {
        setMessages(response.data.messages);
      }
    } catch (error) {
      console.error("Failed to fetch messages:", error);
    }
  };

  const handleSend = async () => {
    if (!draft.trim() || !selectedAdmin) return;
    
    setIsLoading(true);
    try {
      // Send message with the admin's department
      await sendChatMessage(selectedAdmin.department, selectedAdmin.username, draft.trim());
      setDraft("");
      // Immediately fetch updated messages
      await fetchMessages();
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="space-y-8">
      <Navbar title="Department Chat" subtitle="Inter-Department Communication" />

      <div className="bg-white border border-slate-200 rounded-2xl p-5 flex flex-col gap-4 max-w-5xl mx-auto">
        <div className="border-b border-slate-200 pb-3">
          <h2 className="text-lg font-semibold text-slate-900">All Departments Chat</h2>
          <p className="text-sm text-slate-500 mt-1">
            Messages from Pharmacy, Radiology, General Ward, and Administration
          </p>
        </div>
        
        <ChatPanel
          messages={messages}
          currentUsername={selectedAdmin?.username}
        />
        
        <div className="flex gap-3 pt-3 border-t border-slate-200">
          <input
            className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button
            className="px-6 py-2.5 rounded-xl bg-blue-600 text-white text-sm font-semibold disabled:opacity-50 hover:bg-blue-700 transition"
            onClick={handleSend}
            disabled={isLoading || !draft.trim()}
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeptChat;
