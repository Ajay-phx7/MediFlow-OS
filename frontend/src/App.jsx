import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import {
  CalendarCheck,
  ClipboardList,
  FileText,
  LayoutGrid,
  LineChart,
  Map,
  MessagesSquare,
  Pill,
  ShieldAlert,
  Stethoscope,
  UserPlus,
  Users,
} from "lucide-react";

import Sidebar from "./components/Sidebar.jsx";
import Home from "./pages/Home.jsx";
import AdminDashboard from "./pages/admin/AdminDashboard.jsx";
import AdminLogin from "./pages/admin/AdminLogin.jsx";
import CreateAccount from "./pages/admin/CreateAccount.jsx";
import MedicineInventory from "./pages/admin/MedicineInventory.jsx";
import QueueManager from "./pages/admin/QueueManager.jsx";
import SurgePrediction from "./pages/admin/SurgePrediction.jsx";
import LiveMap from "./pages/admin/LiveMap.jsx";
import DeptChat from "./pages/admin/DeptChat.jsx";
import EmergencyControl from "./pages/admin/EmergencyControl.jsx";
import DoctorDashboard from "./pages/doctor/DoctorDashboard.jsx";
import PatientList from "./pages/doctor/PatientList.jsx";
import AIScribe from "./pages/doctor/AIScribe.jsx";
import PatientDashboard from "./pages/patient/PatientDashboard.jsx";
import BookAppointment from "./pages/patient/BookAppointment.jsx";
import HealthReport from "./pages/patient/HealthReport.jsx";
import DoctorLogin from "./pages/doctor/DoctorLogin.jsx";
import PatientLogin from "./pages/patient/PatientLogin.jsx";
import PatientSignup from "./pages/patient/PatientSignup.jsx";
import { AppContext } from "./context/AppContext.jsx";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";

const RoleLayout = ({ title, items, role }) => {
  const navigate = useNavigate();
  const { setActiveRole } = useContext(AppContext);

  const handleRoleChange = (newRole) => {
    setActiveRole(newRole);
    navigate(`/${newRole}/login`);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      <Sidebar
        title={title}
        items={items}
        currentRole={role}
        onRoleChange={handleRoleChange}
      />
      <main className="flex-1 p-6 sm:p-8">
        <Outlet />
      </main>
    </div>
  );
};

const DoctorRoute = ({ children }) => {
  const { selectedDoctor } = useContext(AppContext);

  if (!selectedDoctor) {
    return <Navigate to="/doctor/login" replace />;
  }

  return children;
};

const AdminCreateRoute = ({ children }) => {
  const { selectedAdmin } = useContext(AppContext);

  if (selectedAdmin?.department !== "Administration") {
    return <Navigate to="/admin" replace />;
  }

  return children;
};

const PatientRoute = ({ children }) => {
  const { selectedPatient } = useContext(AppContext);

  if (!selectedPatient) {
    return <Navigate to="/patient/login" replace />;
  }

  return children;
};

const doctorItems = [
  { to: "/doctor", label: "Dashboard", icon: LayoutGrid, end: true },
  { to: "/doctor/patients", label: "My Patients", icon: Users },
  { to: "/doctor/ai-scribe", label: "AI Scribe", icon: Stethoscope },
];

const patientItems = [
  { to: "/patient", label: "Dashboard", icon: LayoutGrid, end: true },
  { to: "/patient/book", label: "Book Appointment", icon: CalendarCheck },
  { to: "/patient/health-report", label: "My Health Report", icon: FileText },
];

const App = () => {
  const { selectedAdmin } = useContext(AppContext);
  const canCreateAccounts = selectedAdmin?.department === "Administration";

  const adminItems = [
    { to: "/admin", label: "Dashboard", icon: LayoutGrid, end: true },
    { to: "/admin/queue", label: "Queue", icon: ClipboardList },
    { to: "/admin/surge", label: "Surge Forecast", icon: LineChart },
    { to: "/admin/live-map", label: "Resource Monitoring", icon: Map },
    { to: "/admin/dept-chat", label: "Dept Chat", icon: MessagesSquare },
    { to: "/admin/emergency", label: "Emergency", icon: ShieldAlert },
  ];

  if (canCreateAccounts) {
    adminItems.splice(1, 0, {
      to: "/admin/create-account",
      label: "Create Account",
      icon: UserPlus,
    });
  }

  if (selectedAdmin?.department === "Pharmacy") {
    adminItems.splice(2, 0, {
      to: "/admin/medicine-inventory",
      label: "Medicine Inventory",
      icon: Pill,
    });
  }

  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/admin/login" element={<AdminLogin />} />
      <Route path="/doctor/login" element={<DoctorLogin />} />
      <Route path="/patient/login" element={<PatientLogin />} />
      <Route path="/patient/signup" element={<PatientSignup />} />

      <Route
        path="/admin"
        element={<RoleLayout title="Admin / Reception" items={adminItems} role="admin" />}
      >
        <Route index element={<AdminDashboard />} />
        <Route
          path="create-account"
          element={
            <AdminCreateRoute>
              <CreateAccount />
            </AdminCreateRoute>
          }
        />
        <Route path="medicine-inventory" element={<MedicineInventory />} />
        <Route path="queue" element={<QueueManager />} />
        <Route path="surge" element={<SurgePrediction />} />
        <Route path="live-map" element={<LiveMap />} />
        <Route path="dept-chat" element={<DeptChat />} />
        <Route path="emergency" element={<EmergencyControl />} />
      </Route>

      <Route
        path="/doctor"
        element={<RoleLayout title="Doctor" items={doctorItems} role="doctor" />}
      >
        <Route index element={<DoctorRoute><DoctorDashboard /></DoctorRoute>} />
        <Route path="patients" element={<DoctorRoute><PatientList /></DoctorRoute>} />
        <Route path="ai-scribe" element={<DoctorRoute><AIScribe /></DoctorRoute>} />
      </Route>

      <Route
        path="/patient"
        element={<RoleLayout title="Patient" items={patientItems} role="patient" />}
      >
        <Route index element={<PatientRoute><PatientDashboard /></PatientRoute>} />
        <Route path="book" element={<PatientRoute><BookAppointment /></PatientRoute>} />
        <Route path="health-report" element={<PatientRoute><HealthReport /></PatientRoute>} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
