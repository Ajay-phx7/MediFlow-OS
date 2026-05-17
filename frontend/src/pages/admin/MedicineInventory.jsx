import { useMemo, useState } from "react";

import Navbar from "../../components/Navbar.jsx";

const MedicineInventory = () => {
  const [search, setSearch] = useState("");

  const inventory = useMemo(
    () => [
      {
        id: 1,
        name: "Amoxicillin",
        category: "Antibiotic",
        status: "In stock",
        stock: 240,
        reorder_level: 80,
        unit: "caps",
        expiry_date: "2026-02-15",
      },
      {
        id: 2,
        name: "Paracetamol",
        category: "Analgesic",
        status: "In stock",
        stock: 520,
        reorder_level: 150,
        unit: "tabs",
        expiry_date: "2027-01-05",
      },
      {
        id: 3,
        name: "Ibuprofen",
        category: "NSAID",
        status: "Low stock",
        stock: 65,
        reorder_level: 120,
        unit: "tabs",
        expiry_date: "2026-09-30",
      },
      {
        id: 4,
        name: "Metformin",
        category: "Diabetes",
        status: "In stock",
        stock: 310,
        reorder_level: 100,
        unit: "tabs",
        expiry_date: "2026-12-12",
      },
      {
        id: 5,
        name: "Amlodipine",
        category: "Cardiology",
        status: "In stock",
        stock: 190,
        reorder_level: 90,
        unit: "tabs",
        expiry_date: "2026-11-18",
      },
      {
        id: 6,
        name: "Atorvastatin",
        category: "Lipid control",
        status: "Low stock",
        stock: 70,
        reorder_level: 120,
        unit: "tabs",
        expiry_date: "2027-03-22",
      },
      {
        id: 7,
        name: "Salbutamol",
        category: "Respiratory",
        status: "In stock",
        stock: 130,
        reorder_level: 60,
        unit: "inhalers",
        expiry_date: "2026-08-08",
      },
      {
        id: 8,
        name: "Omeprazole",
        category: "Gastroenterology",
        status: "In stock",
        stock: 210,
        reorder_level: 90,
        unit: "caps",
        expiry_date: "2027-05-14",
      },
      {
        id: 9,
        name: "Ceftriaxone",
        category: "Antibiotic",
        status: "Critical",
        stock: 28,
        reorder_level: 80,
        unit: "vials",
        expiry_date: "2026-06-02",
      },
      {
        id: 10,
        name: "Insulin Glargine",
        category: "Endocrine",
        status: "Low stock",
        stock: 40,
        reorder_level: 70,
        unit: "pens",
        expiry_date: "2026-10-20",
      },
    ],
    []
  );

  const filteredInventory = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return inventory;
    return inventory.filter((item) => item.name.toLowerCase().includes(term));
  }, [inventory, search]);

  return (
    <div className="space-y-8">
      <Navbar title="Medicine Inventory" subtitle="Pharmacy overview" />

      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="relative w-full max-w-md">
          <input
            className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm"
            placeholder="Search medicines"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>
        <button
          type="button"
          className="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-500"
          disabled
        >
          Add Medicine
        </button>
      </div>

      <div className="rounded-2xl bg-white border border-slate-200 p-6">
        <div className="grid grid-cols-1 gap-4">
          {filteredInventory.map((item) => (
            <div key={item.id} className="rounded-xl border border-slate-200 p-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-slate-900">{item.name}</p>
                  <p className="text-xs text-slate-500 mt-1">{item.category}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                  {item.status}
                </span>
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-500 sm:grid-cols-4">
                <div>
                  <p className="font-semibold text-slate-600">Stock</p>
                  <p>{item.stock} {item.unit}</p>
                </div>
                <div>
                  <p className="font-semibold text-slate-600">Reorder level</p>
                  <p>{item.reorder_level} {item.unit}</p>
                </div>
                <div>
                  <p className="font-semibold text-slate-600">Expiry</p>
                  <p>{item.expiry_date}</p>
                </div>
              </div>
            </div>
          ))}
          {filteredInventory.length === 0 && (
            <p className="text-sm text-slate-500">No medicines match your search.</p>
          )}
        </div>
        <p className="mt-4 text-xs text-slate-400">
          Add Medicine is a placeholder button for future inventory updates.
        </p>
      </div>
    </div>
  );
};

export default MedicineInventory;
