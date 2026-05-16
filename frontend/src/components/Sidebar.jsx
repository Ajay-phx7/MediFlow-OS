import { NavLink } from "react-router-dom";

const Sidebar = ({ items, title }) => {
  return (
    <aside className="bg-slate-900 text-slate-100 sm:w-64 w-16 min-h-screen flex flex-col">
      <div className="px-4 py-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold">
            M
          </div>
          <div className="hidden sm:block">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">MediCore</p>
            <h1 className="text-lg font-semibold">{title}</h1>
          </div>
        </div>
      </div>
      <nav className="flex-1 px-2 py-6 space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 px-3 py-3 rounded-xl transition",
                  isActive
                    ? "bg-slate-800 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white",
                ].join(" ")
              }
              end={item.end}
            >
              <Icon className="h-5 w-5" />
              <span className="hidden sm:inline text-sm font-medium">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
      <div className="px-4 py-4 text-xs text-slate-500 hidden sm:block">
        Dummy prototype v0.1
      </div>
    </aside>
  );
};

export default Sidebar;
