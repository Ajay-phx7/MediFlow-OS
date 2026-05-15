import { useMemo, useState } from "react";

import ChatPanel from "../../components/ChatPanel.jsx";
import Navbar from "../../components/Navbar.jsx";

const DeptChat = () => {
  const departments = ["Pharmacy", "Radiology", "General Ward"];
  const [activeDepartment, setActiveDepartment] = useState("Pharmacy");
  const [messages, setMessages] = useState([
    {
      sender: "Pharmacy",
      text: "Restocking antibiotics in 30 mins.",
      time: "09:30 AM",
      department: "Pharmacy",
    },
    {
      sender: "Radiology",
      text: "CT scan backlog cleared, ready for new slots.",
      time: "09:45 AM",
      department: "Radiology",
    },
    {
      sender: "General Ward",
      text: "Two beds freed in ward B2.",
      time: "10:05 AM",
      department: "General Ward",
    },
  ]);
  const [draft, setDraft] = useState("");

  const filtered = useMemo(
    () => messages.filter((message) => message.department === activeDepartment),
    [messages, activeDepartment]
  );

  const handleSend = () => {
    if (!draft.trim()) return;
    setMessages((prev) => [
      ...prev,
      {
        sender: "Admin",
        text: draft.trim(),
        time: "Now",
        department: activeDepartment,
      },
    ]);
    setDraft("");
  };

  return (
    <div className="space-y-8">
      <Navbar title="Department Chat" subtitle="Internal Messaging" />

      <div className="grid grid-cols-1 lg:grid-cols-[240px_1fr] gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-4 space-y-3">
          {departments.map((dept) => (
            <button
              key={dept}
              className={`w-full text-left px-3 py-2 rounded-xl text-sm font-medium transition ${
                activeDepartment === dept
                  ? "bg-blue-600 text-white"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
              onClick={() => setActiveDepartment(dept)}
            >
              {dept}
            </button>
          ))}
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-5 flex flex-col gap-4">
          <ChatPanel messages={filtered} />
          <div className="flex gap-3">
            <input
              className="flex-1 border border-slate-200 rounded-xl px-3 py-2 text-sm"
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder={`Message ${activeDepartment}`}
            />
            <button
              className="px-4 py-2 rounded-xl bg-blue-600 text-white text-sm font-semibold"
              onClick={handleSend}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeptChat;
