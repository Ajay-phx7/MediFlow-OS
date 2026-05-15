import Badge from "./Badge.jsx";

const QueueTable = ({ rows, onMarkDone }) => {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-slate-500">
          <tr>
            <th className="px-4 py-3 font-medium">Patient Name</th>
            <th className="px-4 py-3 font-medium">Token No.</th>
            <th className="px-4 py-3 font-medium">Dept</th>
            <th className="px-4 py-3 font-medium">Wait Time</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => {
            const tone = row.status.toLowerCase().includes("waiting")
              ? "waiting"
              : row.status.toLowerCase().includes("consultation")
              ? "consultation"
              : "done";

            return (
              <tr key={row.token} className="border-t border-slate-100">
                <td className="px-4 py-3 font-medium text-slate-900">{row.name}</td>
                <td className="px-4 py-3 text-slate-600">{row.token}</td>
                <td className="px-4 py-3 text-slate-600">{row.department}</td>
                <td className="px-4 py-3 text-slate-600">{row.wait_time_min} min</td>
                <td className="px-4 py-3">
                  <Badge label={row.status} tone={tone} />
                </td>
                <td className="px-4 py-3">
                  <button
                    className="text-xs font-semibold text-blue-600 hover:text-blue-700 disabled:text-slate-400"
                    disabled={row.status === "Done"}
                    onClick={() => onMarkDone(row.token)}
                  >
                    Mark Done
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default QueueTable;
