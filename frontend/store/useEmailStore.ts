import { create } from 'zustand';
import { api } from '@/lib/api';
import { toast } from 'sonner';

export interface Email {
    id: string;
    gmail_id: string;
    thread_id?: string;
    from: string;
    subject: string;
    snippet: string;
    timestamp: string;
    isRead: boolean;
    labels: string[];
    score: number;
    summary?: string;
    priority?: 'Urgent' | 'High' | 'Normal' | 'Low'; // Derived helper
}

interface EmailState {
    emails: Email[];
    isLoading: boolean;
    selectedCategory: string;

    fetchEmails: (category?: string) => Promise<void>;
    syncEmails: (email: string) => Promise<void>;
    setSelectedCategory: (category: string) => void;

    // Optimistic updates (keep these for UI responsiveness)
    archiveEmail: (id: string) => void;
    deleteEmail: (id: string) => void;
    markAsRead: (id: string) => void;
}

export const useEmailStore = create<EmailState>((set, get) => ({
    emails: [],
    isLoading: false,
    selectedCategory: 'All',

    fetchEmails: async (category = 'All') => {
        set({ isLoading: true });
        try {
            // API Call
            // Params: skip=0, limit=50, category=...
            const response = await api.get('/gmail/messages', {
                params: { category: category === 'All' ? undefined : category }
            });

            const rawEmails = response.data;

            // Map to UI model if needed (backend matches mostly)
            // Enhance with Priority label based on score
            const emails: Email[] = rawEmails.map((e: any) => ({
                ...e,
                priority: e.score > 80 ? 'Urgent' : e.score > 50 ? 'High' : 'Normal'
            }));

            set({ emails, isLoading: false });
        } catch (error) {
            console.error("Failed to fetch emails", error);
            toast.error("Failed to load inbox");
            set({ isLoading: false });
        }
    },

    syncEmails: async (email: string) => {
        toast.info("Syncing with Gmail...");
        set({ isLoading: true });
        try {
            await api.get('/gmail/sync', { params: { email } });
            toast.success("Sync complete");
            // Refresh list
            await get().fetchEmails(get().selectedCategory);
        } catch (error) {
            console.error("Sync failed", error);
            toast.error("Sync failed");
            set({ isLoading: false });
        }
    },

    setSelectedCategory: (category) => {
        set({ selectedCategory: category });
        get().fetchEmails(category);
    },

    // Optimistic updates
    archiveEmail: (id) =>
        set((state) => ({
            emails: state.emails.filter((email) => email.id !== id)
        })),

    deleteEmail: (id) =>
        set((state) => ({
            emails: state.emails.filter((email) => email.id !== id)
        })),

    markAsRead: (id) =>
        set((state) => ({
            emails: state.emails.map((email) =>
                email.id === id ? { ...email, isRead: true } : email
            ),
        })),
}));
