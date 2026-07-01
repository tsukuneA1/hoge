"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const navigation = [
  { href: "/", label: "時間割" },
  { href: "/courses", label: "授業を探す" },
];

export function Header() {
  const pathname = usePathname();

  return (
    <header className="border-b border-border flex py-4 w-full items-center justify-between px-4 sm:px-10">
      <Link href="/" className="text-lg font-semibold tracking-tight">
        Syllabus Search
      </Link>
      <nav>
        <ul className="flex items-center gap-1">
          {navigation.map((item) => {
            const isActive =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href);

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  aria-current={isActive ? "page" : undefined}
                  className={cn(
                    "inline-flex h-9 items-center px-3 text-sm transition-colors hover:bg-muted",
                    isActive && "bg-muted font-semibold",
                  )}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
}
