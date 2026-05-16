import { useEffect, useMemo, useState } from "react";
import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { AlertTriangle } from "lucide-react";

import Navbar from "../../components/Navbar.jsx";
import { getAdminSurgeForecast, getSurgeForecastCustom } from "../../api/index.js";

const SurgePrediction = () => {
  const [forecast, setForecast] = useState(null);
  const [selectedDays, setSelectedDays] = useState(7);
  const [loading, setLoading] = useState(false);

  const fetchForecast = async (days) => {
    setLoading(true);
    try {
      if (days === 7) {
        const response = await getAdminSurgeForecast();
        setForecast(response.data);
      } else {
        const response = await getSurgeForecastCustom(days);
        setForecast(response.data);
      }
    } catch (error) {
      console.error("Error fetching forecast:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchForecast(7);
  }, []);

  const handleDaysChange = (days) => {
    setSelectedDays(days);
    fetchForecast(days);
  };

  const chartData = useMemo(() => {
    if (!forecast) return [];
    return forecast.dates.map((date, index) => ({
      date,
      predicted: forecast.predicted[index],
      upper: forecast.upper[index],
      lower: forecast.lower[index],
    }));
  }, [forecast]);

  const isHighSurge = useMemo(() => {
    if (!forecast) return false;
    return forecast.predicted.some((value) => value > forecast.threshold);
  }, [forecast]);

  const peakDay = useMemo(() => {
    if (!forecast) return null;
    const maxIndex = forecast.predicted.indexOf(Math.max(...forecast.predicted));
    return {
      date: forecast.dates[maxIndex],
      value: forecast.predicted[maxIndex],
      exceedsThreshold: forecast.predicted[maxIndex] > forecast.threshold,
    };
  }, [forecast]);

  const today = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="space-y-8">
      <Navbar title="Surge Forecast" subtitle="AI Demand Prediction" />

      {isHighSurge && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-2xl p-4">
          High surge expected in the next {selectedDays} days. Prepare staffing and beds.
        </div>
      )}

      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <div className="flex gap-2 mb-6">
          {[7, 14, 30].map((days) => (
            <button
              key={days}
              onClick={() => handleDaysChange(days)}
              disabled={loading}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                selectedDays === days
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {days} Days
            </button>
          ))}
        </div>

        <div className="h-[360px]">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData}>
              <CartesianGrid strokeDasharray="4 4" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis />
              <Tooltip />
              <ReferenceLine
                y={forecast?.threshold ?? 120}
                stroke="#ef4444"
                strokeDasharray="4 4"
                label={{ value: "Surge Threshold", position: "right", fill: "#ef4444" }}
              />
              <Area
                type="monotone"
                dataKey="upper"
                stroke="none"
                fill="#93c5fd"
                fillOpacity={0.2}
              />
              <Area
                type="monotone"
                dataKey="lower"
                stroke="none"
                fill="#93c5fd"
                fillOpacity={0.2}
              />
              <Line
                type="monotone"
                dataKey="predicted"
                stroke="#2563eb"
                strokeWidth={2}
                dot={{ fill: "#2563eb", r: 3 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {peakDay && (
        <div
          className={`rounded-2xl p-6 border-2 ${
            peakDay.exceedsThreshold
              ? "bg-red-50 border-red-300"
              : "bg-green-50 border-green-300"
          }`}
        >
          <div className="flex items-start gap-4">
            {peakDay.exceedsThreshold && (
              <AlertTriangle className="h-6 w-6 text-red-600 flex-shrink-0 mt-1" />
            )}
            <div className="flex-1">
              <h3
                className={`text-lg font-semibold mb-2 ${
                  peakDay.exceedsThreshold ? "text-red-900" : "text-green-900"
                }`}
              >
                {peakDay.exceedsThreshold ? "Peak Day Alert" : "No Surge Predicted"}
              </h3>
              {peakDay.exceedsThreshold ? (
                <div className="space-y-2">
                  <p className="text-red-800">
                    <span className="font-semibold">Date:</span> {peakDay.date}
                  </p>
                  <p className="text-red-800">
                    <span className="font-semibold">Predicted Count:</span> {peakDay.value}
                  </p>
                  <p className="text-red-800 mt-3">
                    <span className="font-semibold">Recommended:</span> Schedule additional staff
                    and open overflow ward.
                  </p>
                </div>
              ) : (
                <p className="text-green-800">
                  No surge days predicted in this window. Current capacity is sufficient.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-600 text-xs rounded-full">
          <span>
            {forecast?.model_info?.model_type || "Simulated"} ·
            Last trained: {forecast?.model_info?.last_trained || today}
            {forecast?.model_info?.accuracy_mape && ` · MAPE: ${forecast.model_info.accuracy_mape}%`}
          </span>
        </div>
      </div>
    </div>
  );
};

export default SurgePrediction;

// Made with Bob
