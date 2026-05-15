const ChatPanel = ({ messages }) => {
  return (
    <div className="flex flex-col gap-3">
      {messages.map((message, index) => (
        <div
          key={`${message.sender}-${index}`}
          className="bg-slate-50 border border-slate-200 rounded-xl p-3"
        >
          <div className="flex items-center justify-between">
            <p className="text-sm font-semibold text-slate-900">{message.sender}</p>
            <span className="text-xs text-slate-400">{message.time}</span>
          </div>
          <p className="text-sm text-slate-600 mt-2">{message.text}</p>
        </div>
      ))}
    </div>
  );
};

export default ChatPanel;
