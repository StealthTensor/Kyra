import { create } from 'zustand';
import { api } from '@/lib/api';
import { toast } from 'sonner';

interface DigestState {
    digest: string | null;
    isLoading: boolean;
    fetchLatestDigest: (email: string) => Promise<void>;
    generateDigest: (user_id: string, email: string) => Promise<void>;
}

export const useDigestStore = create<DigestState>((set) => ({
    digest: null,
    isLoading: false,

    fetchLatestDigest: async (email: string) => {
        set({ isLoading: true });
        try {
            const response = await api.get('/digest/latest', { params: { email } });
            if (response.data.found) {
                set({ digest: response.data.content, isLoading: false });
            } else {
                set({ digest: null, isLoading: false });
            }
        } catch (error) {
            console.error("Failed to fetch digest", error);
            set({ isLoading: false });
        }
    },

    generateDigest: async (user_id: string, email: string) => {
        set({ isLoading: true });
        try {
            const response = await api.post('/digest/generate', { user_id, email });
            set({ digest: response.data.content, isLoading: false });
            toast.success("New digest generated");
        } catch (error) {
            console.error("Failed to generate digest", error);
            toast.error("Failed to generate digest");
            set({ isLoading: false });
        }
    }
}));
