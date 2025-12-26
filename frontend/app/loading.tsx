import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
    return (
        <div className="p-4 space-y-6 pt-12 pb-24 max-w-md mx-auto">
            <div className="space-y-2">
                <Skeleton className="h-8 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
            </div>

            <Skeleton className="h-[200px] w-full rounded-xl" />

            <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                    <Skeleton className="h-24 rounded-xl" />
                    <Skeleton className="h-24 rounded-xl" />
                </div>
                <Skeleton className="h-[300px] w-full rounded-xl" />
            </div>
        </div>
    );
}
