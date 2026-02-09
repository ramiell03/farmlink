"use client";

import React, { useEffect } from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarProvider,
} from "@/components/ui/sidebar";
import { 
  HomeIcon, 
  UserIcon, 
  SettingsIcon, 
  BoxIcon, 
  MessageSquare,
  ShoppingCart,
  BarChart3,
  Package,
  Users,
  DollarSign,
  BellIcon
} from "lucide-react";
import { usePathname, useRouter } from "next/navigation";
import { AuthProvider, useAuth } from "@/lib/auth-context";
import { Toaster } from "@/components/ui/sonner";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

function ProtectedLayoutInner({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { role, loading } = useAuth();

  useEffect(() => {
    if (!loading && !role) {
      router.replace("/signin");
    }
  }, [role, loading, router]);

  if (loading) return (
    <div className="flex h-screen items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
    </div>
  );

  const isActive = (path: string) => pathname === path;

  return (
    <SidebarProvider defaultOpen>
      <Sidebar>
        <SidebarContent>
          {/* User Info */}
          <div className="p-4 border-b">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                <span className="text-blue-600 font-semibold">
                  {role?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <p className="font-semibold capitalize">{role} Dashboard</p>
                <p className="text-sm text-gray-500">Welcome back!</p>
              </div>
            </div>
          </div>

          <SidebarMenu>
            {/* Common Navigation for all roles */}
            <SidebarMenuItem>
              <SidebarMenuButton asChild data-active={isActive("/dashboard")}>
                <Link href="/dashboard">
                  <HomeIcon className="w-4 h-4 mr-2" />
                  Dashboard
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>

            {/* Farmer-specific navigation */}
            {role === "farmer" && (
              <>
                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/farmer/listings")}>
                    <Link href="/dashboard/farmer/listings">
                      <Package className="w-4 h-4 mr-2" />
                      My Listings
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/farmer/orders")}>
                    <Link href="/dashboard/farmer/orders">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      Orders
                      <Badge className="ml-2 bg-blue-600">3</Badge>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/farmer/messages")}>
                    <Link href="/dashboard/farmer/messages">
                      <MessageSquare className="w-4 h-4 mr-2" />
                      Messages
                      <Badge className="ml-2 bg-blue-600">5</Badge>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/farmer/analytics")}>
                    <Link href="/dashboard/farmer/analytics">
                      <BarChart3 className="w-4 h-4 mr-2" />
                      Analytics
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </>
            )}

            {/* Admin-specific navigation */}
            {role === "admin" && (
              <>
                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/admin")}>
                    <Link href="/dashboard/admin">
                      <BarChart3 className="w-4 h-4 mr-2" />
                      Overview
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/admin/users")}>
                    <Link href="/dashboard/admin/users">
                      <Users className="w-4 h-4 mr-2" />
                      Users
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/admin/listings")}>
                    <Link href="/dashboard/admin/listings">
                      <Package className="w-4 h-4 mr-2" />
                      All Listings
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/admin/orders")}>
                    <Link href="/dashboard/admin/orders">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      All Orders
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/admin/revenue")}>
                    <Link href="/dashboard/admin/revenue">
                      <DollarSign className="w-4 h-4 mr-2" />
                      Revenue
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </>
            )}

            {/* Buyer-specific navigation */}
            {role === "buyer" && (
              <>
                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/buyer/marketplace")}>
                    <Link href="/dashboard/buyer/marketplace">
                      <Package className="w-4 h-4 mr-2" />
                      Marketplace
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/buyer/orders")}>
                    <Link href="/dashboard/buyer/orders">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      My Orders
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                <SidebarMenuItem>
                  <SidebarMenuButton asChild data-active={isActive("/dashboard/buyer/messages")}>
                    <Link href="/dashboard/buyer/messages">
                      <MessageSquare className="w-4 h-4 mr-2" />
                      Messages
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </>
            )}

            {/* Common navigation for all roles */}
            <div className="mt-4 pt-4 border-t">
              <SidebarMenuItem>
                <SidebarMenuButton asChild data-active={isActive("/dashboard/profile")}>
                  <Link href="/dashboard/profile">
                    <UserIcon className="w-4 h-4 mr-2" />
                    Profile
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton asChild data-active={isActive("/dashboard/notifications")}>
                  <Link href="/dashboard/notifications">
                    <BellIcon className="w-4 h-4 mr-2" />
                    Notifications
                    <Badge className="ml-2 bg-red-600">2</Badge>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>

              <SidebarMenuItem>
                <SidebarMenuButton asChild data-active={isActive("/dashboard/settings")}>
                  <Link href="/dashboard/settings">
                    <SettingsIcon className="w-4 h-4 mr-2" />
                    Settings
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </div>
          </SidebarMenu>
        </SidebarContent>
      </Sidebar>

      <main className="flex-1 p-6 bg-gray-50 min-h-screen overflow-y-auto">
        {children}
      </main>
    </SidebarProvider>
  );
}

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider>
      <ProtectedLayoutInner>{children}</ProtectedLayoutInner>
      <Toaster />
    </AuthProvider>
  );
}