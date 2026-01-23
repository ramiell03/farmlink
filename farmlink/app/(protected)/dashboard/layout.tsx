"use client";

import React from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarProvider,
} from "@/components/ui/sidebar";
import { HomeIcon, UserIcon, SettingsIcon, BoxIcon } from "lucide-react";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <SidebarProvider defaultOpen={true}>
      <Sidebar>
        <SidebarContent>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                asChild
                data-active={pathname === "/dashboard"}
              >
                <a href="/dashboard">
                  <HomeIcon className="inline mr-2" />
                  Home
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                asChild
                data-active={pathname === "/dashboard/products"}
              >
                <a href="/dashboard/products">
                  <BoxIcon className="inline mr-2" />
                  Products
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                asChild
                data-active={pathname === "/dashboard/profile"}
              >
                <a href="/dashboard/profile">
                  <UserIcon className="inline mr-2" />
                  Profile
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                asChild
                data-active={pathname === "/dashboard/settings"}
              >
                <a href="/dashboard/settings">
                  <SettingsIcon className="inline mr-2" />
                  Settings
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarContent>
      </Sidebar>

      <main className="flex-1 p-6 bg-gray-100 min-h-screen">{children}</main>
    </SidebarProvider>
  );
}
