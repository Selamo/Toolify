import { Sidebar } from "@/components/chat/Sidebar";
import { Providers } from "@/components/Providers";

export default function ChatLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <Providers>
            <div className="flex h-screen w-full bg-background overflow-hidden relative">
                <Sidebar />
                <main className="flex-1 h-full min-w-0 bg-background transition-colors duration-300">
                    {children}
                </main>
            </div>
        </Providers>
    );
}
