"use client";

import { useState, useEffect } from "react";
import { FilterPills } from "@/components/mail/FilterPills";
import { EmailCard } from "@/components/mail/EmailCard";
import { EmailDetailDrawer } from "@/components/mail/EmailDetailDrawer";
import { motion } from "framer-motion";
import { useEmailStore, Email } from "@/store/useEmailStore";
import { useAuthStore } from "@/store/useAuthStore";

export default function MailPage() {
    const [selectedEmail, setSelectedEmail] = useState<any | null>(null);
    const { emails, fetchEmails, syncEmails, isLoading, selectedCategory, setSelectedCategory } = useEmailStore();

    useEffect(() => {
        // Initial fetch handled by store or component mount
        fetchEmails(selectedCategory);
    }, [selectedCategory, fetchEmails]);

    const filteredEmails = emails; // Store handles filtering via fetch, or we can filter locally if we fetch 'All'

    const handleArchive = (id: string) => {
        // Optimistic UI update handled by store
        // useEmailStore.getState().archiveEmail(id);
    };

    const handleReply = (id: string) => {
        console.log("Reply to", id);
    };

    const { user } = useAuthStore();
    const handleSync = () => {
        if (user?.email) {
            syncEmails(user.email);
        } else {
            console.warn("Cannot sync: No user email");
        }
    };

    return (
        <div className="flex flex-col h-full bg-zinc-950 pt-4">
            {/* Header */}
            <header className="px-4 pb-2 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-white">Inbox</h1>
                <button
                    onClick={handleSync}
                    className={`p-2 rounded-full hover:bg-zinc-800 ${isLoading ? 'animate-spin' : ''}`}
                >
                    <svg className="w-5 h-5 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                </button>
            </header>

            {/* Filters */}
            <div className="sticky top-0 z-20 bg-zinc-950/80 backdrop-blur-md border-b border-zinc-900">
                <FilterPills
                    activeFilter={selectedCategory}
                    onFilterChange={(cat) => { setSelectedCategory(cat); }}
                />
            </div>

            {/* Email List */}
            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-2 pb-24">
                {isLoading && emails.length === 0 ? (
                    <div className="p-4 space-y-4">
                        {[1, 2, 3].map(i => <div key={i} className="h-24 bg-zinc-900/50 rounded-xl animate-pulse" />)}
                    </div>
                ) : filteredEmails.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-64 text-zinc-500">
                        <p>No emails in {selectedCategory}</p>
                    </div>
                ) : (
                    filteredEmails.map((email) => (
                        <motion.div
                            key={email.id}
                            layout
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, height: 0 }}
                        >
                            <EmailCard
                                email={email}
                                onOpen={setSelectedEmail}
                                onArchive={handleArchive}
                                onReply={handleReply}
                            />
                        </motion.div>
                    ))
                )}
            </div>

            {/* Detail Drawer */}
            {/* Note: Ensure DetailDrawer can handle the Store Email object or cast it */}
            <EmailDetailDrawer
                email={selectedEmail}
                onClose={() => setSelectedEmail(null)}
            />
        </div>
    );
}
