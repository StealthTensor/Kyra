"use client";

import { useEffect, useState, lazy, Suspense } from "react";
import { motion } from 'framer-motion';
import { DailyBriefingCard } from "@/components/home/DailyBriefingCard";
import { PriorityInboxPreview } from "@/components/home/PriorityInboxPreview";
import { QuickStats } from "@/components/home/QuickStats";
import { Card } from "@/components/ui/card";
import { useAuthStore } from "@/store/useAuthStore";
import { api } from "@/lib/api";

const LazyPriorityInboxPreview = lazy(() => Promise.resolve({ default: PriorityInboxPreview }));
const LazyDailyBriefingCard = lazy(() => Promise.resolve({ default: DailyBriefingCard }));

interface DashboardStats {
  urgent_emails: number;
  pending_tasks: number;
  upcoming_events: number;
  total_things: number;
  inbox_health: number;
  total_unread: number;
}

export default function Home() {
  const { user } = useAuthStore();
  const userName = user?.name?.split(' ')[0] || user?.email?.split('@')[0] || "User";
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user?.email) {
      setIsLoading(false);
      return;
    }

    const fetchStats = async () => {
      try {
        setIsLoading(true);
        const response = await api.get(`/dashboard/stats?email=${encodeURIComponent(user.email)}`);
        setStats(response.data);
      } catch (error) {
        console.error("Failed to fetch dashboard stats:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, [user?.email]);

  const totalThings = stats?.total_things ?? 0;
  const thingsText = totalThings === 1 ? "thing" : "things";

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
          {isLoading ? (
            "Loading..."
          ) : (
            <>
              Kyra has <span className="text-white font-medium">{totalThings} {thingsText}</span> for you today.
            </>
          )}
        </p>
      </motion.div>

      {/* Daily Briefing */}
      <section>
        <Suspense fallback={<div className="h-32 bg-zinc-900 rounded-lg animate-pulse" />}>
          <DailyBriefingCard />
        </Suspense>
      </section>

      {/* Quick Stats & Priority Inbox Grid or Stack */}
      <div className="space-y-6">
        <QuickStats />
        <Suspense fallback={<div className="h-48 bg-zinc-900 rounded-lg animate-pulse" />}>
          <PriorityInboxPreview />
        </Suspense>

        {/* Quick Actions */}
        {stats && stats.total_things > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="grid grid-cols-3 gap-3"
          >
            {stats.urgent_emails > 0 && (
              <Card className="bg-red-500/10 border-red-500/20 p-3 text-center">
                <p className="text-2xl font-bold text-red-400">{stats.urgent_emails}</p>
                <p className="text-xs text-zinc-400 mt-1">Urgent</p>
              </Card>
            )}
            {stats.pending_tasks > 0 && (
              <Card className="bg-yellow-500/10 border-yellow-500/20 p-3 text-center">
                <p className="text-2xl font-bold text-yellow-400">{stats.pending_tasks}</p>
                <p className="text-xs text-zinc-400 mt-1">Tasks</p>
              </Card>
            )}
            {stats.upcoming_events > 0 && (
              <Card className="bg-blue-500/10 border-blue-500/20 p-3 text-center">
                <p className="text-2xl font-bold text-blue-400">{stats.upcoming_events}</p>
                <p className="text-xs text-zinc-400 mt-1">Events</p>
              </Card>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
