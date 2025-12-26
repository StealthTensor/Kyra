"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/useAuthStore";
import { useRouter, usePathname } from "next/navigation";
import AppListener from "@/components/AppListener";
import ServiceWorkerRegister from "@/components/sw-register";
import { toast } from "sonner";

export default function AuthSync({ children }: { children: React.ReactNode }) {
    const { isAuthenticated, token, logout } = useAuthStore();
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        // Sync localStorage to Cookies for Middleware
        if (token) {
            document.cookie = `token=${token}; path=/; max-age=86400; SameSite=Strict`;
        } else {
            document.cookie = `token=; path=/; max-age=0;`;
        }
    }, [token]);

    useEffect(() => {
        const isAuthPage = pathname?.startsWith("/auth");

        if (!isAuthenticated && !isAuthPage) {
            // Middleware handles main protection, but this catches clients-side logout
            // router.push("/auth/login");
        }

        if (isAuthenticated && isAuthPage) {
            router.push("/mail");
        }
    }, [isAuthenticated, pathname, router]);

    return (
        <>
            <AppListener />
            <ServiceWorkerRegister />
            {children}
        </>
    );
}
