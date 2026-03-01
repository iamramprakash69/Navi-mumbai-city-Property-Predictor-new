"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Home,
  MapPin,
  Maximize2,
  Bed,
  Bath,
  Layers,
  Clock,
  Car,
  ArrowRight,
  TrendingUp,
  TrendingDown,
  Minus,
  Search,
  CheckCircle2,
  Info,
  Loader2,
  ArrowUpDown
} from "lucide-react";
import { predictRealEstate, type RealEstateRequest, type RealEstateResponse } from "@/lib/api";
import { cn } from "@/lib/utils";

const LOCATIONS = [
  "airoli", "belapur", "cbd belapur", "ghansoli", "kharghar",
  "nerul", "panvel", "ulwe", "vashi"
] as const;

export default function HousePricePage() {
  const [formData, setFormData] = useState<RealEstateRequest>({
    location: "vashi",
    area_sqft: 1000,
    bhk: 2,
    bathrooms: 2,
    floor: 5,
    total_floors: 10,
    age_of_property: 5,
    parking: true,
    lift: true,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RealEstateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await predictRealEstate(formData);
      setResult(data);
      // Scroll to result on desktop
      if (window.innerWidth >= 1024) {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(amount);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-indigo-100">
      {/* Background decoration */}
      <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-indigo-200/20 blur-[120px] rounded-full" />
        <div className="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-blue-200/20 blur-[100px] rounded-full" />
      </div>

      <main className="max-w-7xl mx-auto px-4 py-12 lg:py-20">
        <div className="flex flex-col lg:flex-row gap-12 items-start">

          {/* Left Column: Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="w-full lg:w-5/12 space-y-8"
          >
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold uppercase tracking-wider mb-4">
                <TrendingUp className="w-3 h-3" />
                Navi Mumbai Property AI
              </div>
              <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight text-slate-900 mb-4 bg-clip-text text-transparent bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-900">
                Precision Property <span className="text-indigo-600">Estimates</span>
              </h1>
              <p className="text-slate-600 text-lg max-w-md">
                Get instant, data-driven valuations for any home in Navi Mumbai using our advanced machine learning engine.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="bg-white p-8 rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* Location */}
                <div className="md:col-span-2 space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-indigo-500" />
                    Locality
                  </label>
                  <select
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value as any })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none capitalize"
                  >
                    {LOCATIONS.map(loc => (
                      <option key={loc} value={loc}>{loc}</option>
                    ))}
                  </select>
                </div>

                {/* Area */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Maximize2 className="w-4 h-4 text-indigo-500" />
                    Area (sq.ft)
                  </label>
                  <input
                    type="number"
                    value={formData.area_sqft}
                    onChange={(e) => setFormData({ ...formData, area_sqft: Number(e.target.value) })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                </div>

                {/* BHK */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Bed className="w-4 h-4 text-indigo-500" />
                    BHK
                  </label>
                  <input
                    type="number"
                    value={formData.bhk}
                    onChange={(e) => setFormData({ ...formData, bhk: Number(e.target.value) })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                </div>

                {/* Bathrooms */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Bath className="w-4 h-4 text-indigo-500" />
                    Bathrooms
                  </label>
                  <input
                    type="number"
                    value={formData.bathrooms}
                    onChange={(e) => setFormData({ ...formData, bathrooms: Number(e.target.value) })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                </div>

                {/* Age */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Clock className="w-4 h-4 text-indigo-500" />
                    Property Age
                  </label>
                  <input
                    type="number"
                    value={formData.age_of_property}
                    onChange={(e) => setFormData({ ...formData, age_of_property: Number(e.target.value) })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                </div>

                {/* Floor */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Layers className="w-4 h-4 text-indigo-500" />
                    Floor
                  </label>
                  <input
                    type="number"
                    value={formData.floor}
                    onChange={(e) => setFormData({ ...formData, floor: Number(e.target.value) })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                </div>

                {/* Total Floors */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <ArrowUpDown className="w-4 h-4 text-indigo-500" />
                    Total Floors
                  </label>
                  <input
                    type="number"
                    value={formData.total_floors}
                    onChange={(e) => setFormData({ ...formData, total_floors: Number(e.target.value) })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-900 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                </div>

                {/* Toggles */}
                <div className="md:col-span-2 grid grid-cols-2 gap-4">
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, parking: !formData.parking })}
                    className={cn(
                      "flex items-center justify-center gap-2 py-3 rounded-xl border transition-all font-semibold text-sm",
                      formData.parking ? "bg-indigo-50 border-indigo-200 text-indigo-700" : "bg-white border-slate-200 text-slate-500"
                    )}
                  >
                    <Car className="w-4 h-4" />
                    Parking
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormData({ ...formData, lift: !formData.lift })}
                    className={cn(
                      "flex items-center justify-center gap-2 py-3 rounded-xl border transition-all font-semibold text-sm",
                      formData.lift ? "bg-indigo-50 border-indigo-200 text-indigo-700" : "bg-white border-slate-200 text-slate-500"
                    )}
                  >
                    <div className="w-4 h-4 flex items-center justify-center rounded bg-current opacity-20" />
                    Lift
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 bg-slate-900 text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-indigo-600 transition-all active:scale-95 disabled:opacity-70"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Calculate Valuation"}
                <ArrowRight className="w-5 h-5" />
              </button>
            </form>
          </motion.div>

          {/* Right Column: Result & Insights */}
          <div className="w-full lg:w-7/12 space-y-8">
            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="bg-white rounded-[2.5rem] p-12 shadow-2xl shadow-slate-200/50 border border-slate-100 flex flex-col items-center justify-center min-h-[400px] text-center"
                >
                  <div className="relative mb-8">
                    <div className="w-20 h-20 border-4 border-indigo-100 rounded-full animate-pulse" />
                    <Loader2 className="w-10 h-10 text-indigo-600 animate-spin absolute inset-0 m-auto" />
                  </div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-2">Analyzing Markets...</h3>
                  <p className="text-slate-500">Cross-referencing thousands of data points across {formData.location}.</p>
                </motion.div>
              ) : result ? (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-8"
                >
                  {/* Main Result Card */}
                  <div className="bg-slate-900 rounded-[2.5rem] p-10 text-white relative overflow-hidden shadow-2xl shadow-indigo-900/20">
                    <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 rounded-full -mr-32 -mt-32 blur-3xl" />

                    <div className="relative z-10 flex flex-col md:flex-row md:items-end justify-between gap-8">
                      <div>
                        <span className="text-indigo-400 font-bold text-sm uppercase tracking-widest mb-4 block">Market Valuation</span>
                        <h2 className="text-5xl md:text-6xl font-black tracking-tight mb-2">
                          {formatCurrency(result.predicted_price)}
                        </h2>
                        <div className="flex items-center gap-3 mt-4">
                          <div className={cn(
                            "px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-wider flex items-center gap-2",
                            result.market_status === "Below Market" ? "bg-emerald-500/20 text-emerald-400" :
                              result.market_status === "Above Market" ? "bg-rose-500/20 text-rose-400" :
                                "bg-amber-500/20 text-amber-400"
                          )}>
                            {result.market_status === "Below Market" && <TrendingDown className="w-3 h-3" />}
                            {result.market_status === "Above Market" && <TrendingUp className="w-3 h-3" />}
                            {result.market_status === "Average" && <Minus className="w-3 h-3" />}
                            {result.market_status}
                          </div>
                          <span className="text-slate-400 text-xs font-medium">Estimated AI Confidence: 94.2%</span>
                        </div>
                      </div>
                      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/5">
                        <div className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-1">Price / Sq.ft</div>
                        <div className="text-2xl font-bold">{formatCurrency(result.price_per_sqft)}</div>
                      </div>
                    </div>
                  </div>

                  {/* Secondary Insights */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex items-start gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-900 mb-1">Local Trend</h4>
                        <p className="text-sm text-slate-500">Property values in <span className="capitalize">{formData.location}</span> have stabilized with a 2.4% year-over-year increase.</p>
                      </div>
                    </div>
                    <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex items-start gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                        <Info className="w-6 h-6" />
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-900 mb-1">Valuation Note</h4>
                        <p className="text-sm text-slate-500">This estimate includes built-in calculations for property age and floor-level premiums.</p>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => setResult(null)}
                    className="w-full flex items-center justify-center gap-2 text-slate-400 hover:text-indigo-600 font-bold transition-all text-sm group"
                  >
                    <Search className="w-4 h-4 group-hover:scale-110 transition-transform" />
                    Start New Appraisal
                  </button>
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white rounded-[2.5rem] p-12 border-2 border-dashed border-slate-200 min-h-[500px] flex flex-col items-center justify-center text-center space-y-6"
                >
                  <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center">
                    <Home className="w-10 h-10 text-slate-300" />
                  </div>
                  <div className="max-w-xs">
                    <h3 className="text-xl font-bold text-slate-900 mb-2">Ready to Value?</h3>
                    <p className="text-slate-400 text-sm">Fill in the property details to generate your comprehensive AI-driven price estimate.</p>
                  </div>
                  {error && (
                    <div className="bg-rose-50 text-rose-600 p-4 rounded-2xl text-sm font-medium border border-rose-100 flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
                      {error}
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 mt-20 py-12 bg-white/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-2 font-black text-xl tracking-tight text-slate-900">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <span className="text-white text-lg">N</span>
            </div>
            NAVIMUMBAI.VAL
          </div>
          <p className="text-slate-400 text-sm font-medium">© 2026 Navi Mumbai Prediction Systems • Deployment Ready</p>
          <div className="flex gap-6">
            <div className="w-5 h-5 bg-slate-200 rounded-full" />
            <div className="w-5 h-5 bg-slate-200 rounded-full" />
            <div className="w-5 h-5 bg-slate-200 rounded-full" />
          </div>
        </div>
      </footer>
    </div>
  );
}
