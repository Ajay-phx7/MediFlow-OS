const TONE_MAP = {
  waiting: "bg-amber-100 text-amber-700",
  consultation: "bg-blue-100 text-blue-700",
  done: "bg-green-100 text-green-700",
  low: "bg-green-100 text-green-700",
  moderate: "bg-amber-100 text-amber-700",
  high: "bg-red-100 text-red-700",
};

const Badge = ({ label, tone }) => {
  return (
    <span
      className={[
        "px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide",
        TONE_MAP[tone] || "bg-slate-100 text-slate-600",
      ].join(" ")}
    >
      {label}
    </span>
  );
};

export default Badge;
