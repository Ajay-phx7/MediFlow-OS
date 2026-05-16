import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import Navbar from "../../components/Navbar.jsx";
import { getAdminSurgeForecast } from "../../api/index.js";

const SurgePrediction = () => {
  const [forecast, setForecast] = useState(null);

  useEffect(() => {
    getAdminSurgeForecast().then((response) => setForecast(response.data));
  }, []);

  const chartData = useMemo(() => {
    if (!forecast) return [];
    return forecast.dates.map((date, index) => ({
      date,
      predicted: forecast.predicted[index],
    }));
  }, [forecast]);

  const isHighSurge = useMemo(() => {
    if (!forecast) return false;
    return forecast.predicted.some((value) => value > forecast.threshold);
  }, [forecast]);

  return (
    <div className="space-y-8">
      <Navbar title="Surge Forecast" subtitle="AI Demand Prediction" />

      {isHighSurge && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-2xl p-4">
          High surge expected in the next 7 days. Prepare staffing and beds.
        </div>
      )}

      <div className="bg-white border border-slate-200 rounded-2xl p-6 h-[360px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="4 4" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis />
            <Tooltip />
            <ReferenceLine
              y={forecast?.threshold ?? 0}
              stroke="#ef4444"
              strokeDasharray="4 4"
              label={{ value: "High Surge", position: "right", fill: "#ef4444" }}
            />
            <Bar dataKey="predicted" fill="#2563eb" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SurgePrediction;
