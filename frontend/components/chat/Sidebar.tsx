import Link from "next/link";
import {
    Plus,
    Search,
    LayoutGrid,
    FolderOpen,
    Settings,
    LogOut,
    MessageSquare,
    type LucideIcon
} from "lucide-react";
import { ThemeToggle } from "../ThemeToggle";

interface NavItem {
    icon: LucideIcon;
    label: string;
    href: string;
    active?: boolean;
}

const navItems: NavItem[] = [
    { icon: Search, label: "Search", href: "#" },
    { icon: LayoutGrid, label: "Apps", href: "#" },
    { icon: MessageSquare, label: "Chats", href: "#", active: true },
    { icon: FolderOpen, label: "Files", href: "#" },
];

export function Sidebar() {
    return (
        <aside className="w-16 md:w-20 lg:w-20 border-r border-border bg-card flex flex-col items-center py-6 h-screen select-none z-20 transition-colors duration-300">
            {/* Logo Area */}
            <div className="mb-8">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center text-white font-bold text-xl shadow-lg ring-2 ring-orange-500/20">
                    T
                </div>
            </div>

            {/* New Chat Action */}
            <button className="mb-8 p-3 rounded-xl bg-muted hover:bg-muted/80 transition-colors group">
                <Plus className="w-6 h-6 text-foreground group-hover:scale-110 transition-transform" />
            </button>

            {/* Main Navigation */}
            <nav className="flex-1 flex flex-col gap-4 w-full items-center">
                {navItems.map((item, index) => (
                    <Link
                        key={index}
                        href={item.href}
                        className={`p-3 rounded-xl transition-all relative group
              ${item.active
                                ? "text-primary bg-primary/10"
                                : "text-muted-foreground hover:text-foreground hover:bg-muted"
                            }`}
                    >
                        <item.icon className="w-6 h-6" />

                        {/* Tooltip */}
                        <span className="absolute left-14 bg-popover text-popover-foreground px-2 py-1 rounded text-sm opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none shadow-md border border-border bg-card">
                            {item.label}
                        </span>
                    </Link>
                ))}
            </nav>

            {/* Bottom Actions */}
            <div className="flex flex-col gap-4 items-center">
                <ThemeToggle />
                <button className="p-3 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted transition-colors">
                    <Settings className="w-6 h-6" />
                </button>
                <button className="p-3 rounded-xl text-muted-foreground hover:text-red-500 hover:bg-red-500/10 transition-colors">
                    <LogOut className="w-6 h-6" />
                </button>

                {/* User Avatar Placeholder */}
                <div className="mt-2 w-10 h-10 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 border-2 border-background ring-2 ring-border" />
            </div>
        </aside>
    );
}
