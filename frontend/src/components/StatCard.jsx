const StatCard = ({ label, value, icon: Icon, accent = "text-primary-container" }) => {
  return (
    <div className="glass-panel rounded-xl p-4 glow-hover transition-all duration-300 cursor-default">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-data-label text-xs text-on-surface-variant uppercase tracking-wider">
            {label}
          </p>
          <p className="font-metric-xl text-3xl font-bold text-primary mt-2">
            {value}
          </p>
        </div>
        <div className={`h-12 w-12 rounded-xl bg-surface-variant flex items-center justify-center ${accent}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  );
};

export default StatCard;

// Made with Bob
