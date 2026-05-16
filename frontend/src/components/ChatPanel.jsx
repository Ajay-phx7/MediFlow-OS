const ChatPanel = ({ messages, currentUsername }) => {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const getDepartmentColor = (department) => {
    const colors = {
      "Pharmacy": "bg-green-100 text-green-800 border-green-200",
      "Radiology": "bg-purple-100 text-purple-800 border-purple-200",
      "General Ward": "bg-amber-100 text-amber-800 border-amber-200",
      "Administration": "bg-cyan-100 text-cyan-800 border-cyan-200"
    };
    return colors[department] || "bg-gray-100 text-gray-800 border-gray-200";
  };

  return (
    <div className="flex flex-col gap-3 max-h-[500px] overflow-y-auto px-2">
      {messages.length === 0 ? (
        <div className="text-center py-12 text-slate-400">
          <p className="text-sm">No messages yet. Start the conversation!</p>
        </div>
      ) : (
        messages.map((message, index) => {
          const isCurrentUser = message.sender_username === currentUsername;
          return (
            <div
              key={`${message.id || index}`}
              className={`rounded-xl p-3 ${
                isCurrentUser
                  ? "bg-blue-50 border border-blue-200 ml-8"
                  : "bg-slate-50 border border-slate-200 mr-8"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <p className={`text-sm font-semibold ${
                    isCurrentUser ? "text-blue-900" : "text-slate-900"
                  }`}>
                    {isCurrentUser ? "You" : message.sender_username}
                  </p>
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${getDepartmentColor(message.department)}`}>
                    {message.department}
                  </span>
                </div>
                <span className="text-xs text-slate-400">
                  {formatTime(message.timestamp)}
                </span>
              </div>
              <p className={`text-sm ${
                isCurrentUser ? "text-blue-800" : "text-slate-600"
              }`}>
                {message.message_text}
              </p>
            </div>
          );
        })
      )}
    </div>
  );
};

export default ChatPanel;
