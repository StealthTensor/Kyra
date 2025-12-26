"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuthStore } from "@/store/useAuthStore";
import { toast } from "sonner";
import { Skeleton } from "@/components/ui/skeleton";

function CallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const login = useAuthStore((state) => state.login);

    useEffect(() => {
        const token = searchParams.get("token");
        const name = searchParams.get("name");
        const email = searchParams.get("email");
        const id = searchParams.get("user_id");

        if (token && email && id) {
            login(
                {
                    id: id,
                    name: name || email.split("@")[0],
                    email: email,
                    avatar: `https://ui-avatars.com/api/?name=${name || email}&background=random`,
                },
                token
            );
            toast.success("Login successful");
            router.push("/mail");
        } else {
            // toast.error("Invalid login callback");
            // router.push("/auth/login");
        }
    }, [searchParams, login, router]);

    return (
        <div className="flex h-screen items-center justify-center space-y-4 flex-col">
            <Skeleton className="h-12 w-12 rounded-full" />
            <p className="text-zinc-500">Authenticating...</p>
        </div>
    );
}

export default function AuthCallbackPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <CallbackContent />
        </Suspense>
    );
}
