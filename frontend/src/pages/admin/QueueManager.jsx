import { useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import QueueTable from "../../components/QueueTable.jsx";
import { getAdminQueue } from "../../api/index.js";

const QueueManager = () => {
  const [queue, setQueue] = useState([]);

  useEffect(() => {
    getAdminQueue().then((response) => setQueue(response.data.queue));
  }, []);

  const handleMarkDone = (token) => {
    setQueue((prev) =>
      prev.map((item) =>
        item.token === token ? { ...item, status: "Done" } : item
      )
    );
  };

  return (
    <div className="space-y-8">
      <Navbar title="Queue Manager" subtitle="Live Token Queue" />
      <QueueTable rows={queue} onMarkDone={handleMarkDone} />
    </div>
  );
};

export default QueueManager;
