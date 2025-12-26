"use client";

import { motion } from 'framer-motion';
import { DailyBriefingCard } from "@/components/home/DailyBriefingCard";
import { PriorityInboxPreview } from "@/components/home/PriorityInboxPreview";
import { QuickStats } from "@/components/home/QuickStats";
import { useAuthStore } from "@/store/useAuthStore";

export default function Home() {
  const { user } = useAuthStore();
  const userName = user?.name?.split(' ')[0] || "Trinai";

  return (
    <div className="p-4 space-y-6 pt-12 pb-24 max-w-md mx-auto">
      {/* Top Section */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="space-y-1"
      >
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
          Good Morning, {userName}.
        </h1>
        <p className="text-zinc-400 text-sm">
          Kyra has <span className="text-white font-medium">3 things</span> for you today.
        </p>
      </motion.div>

      {/* Daily Briefing */}
      <section>
        <DailyBriefingCard />
      </section>

      {/* Quick Stats & Priority Inbox Grid or Stack */}
      <div className="space-y-6">
        <QuickStats />
        <PriorityInboxPreview />
      </div>
    </div>
  );
}
