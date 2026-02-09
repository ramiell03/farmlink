"use client";

import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Wheat, DollarSign, ShoppingCart, Loader2 } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";

const AdminPage = () => {
  const { role, loading, logout } = useAuth();
  const router = useRouter();
  const [isFetching, setIsFetching] = useState(false);

  const [stats, setStats] = useState([
    { title: "Total Users", value: "—", icon: Users },
    { title: "Total Listings", value: "—", icon: Wheat },
    { title: "Total Orders", value: "—", icon: ShoppingCart },
    { title: "Revenue (FCFA)", value: "—", icon: DollarSign },
  ]);

  useEffect(() => {
    // Don't do anything while loading
    if (loading) return;

    // Check if user is admin
    if (role !== "admin") {
      // Redirect to appropriate dashboard based on role
      if (role === "farmer") {
        router.push("/dashboard/farmer");
      } else if (role === "buyer") {
        router.push("/dashboard/buyer");
      } else {
        router.push("/signin");
      }
      return;
    }

    // Fetch stats for admin
    const fetchStats = async () => {
      setIsFetching(true);
      try {
        console.log("Fetching admin stats...");
        const res = await fetch("/api/admin/stats", {
          credentials: 'include',
          headers: { 
            "Content-Type": "application/json"
          },
        });

        console.log("API Response status:", res.status);

        // Handle unauthorized (401) - token expired
        if (res.status === 401) {
          console.error("Token expired or invalid");
          logout();
          return;
        }

        // Handle other errors
        if (!res.ok) {
          let errorData = {};
          try {
            errorData = await res.json();
          } catch {
            errorData = { error: `HTTP ${res.status}` };
          }
          console.error(`Failed to load stats: ${res.status}`, errorData);
          
          // For development, use mock data if API fails
          if (process.env.NODE_ENV === "development") {
            console.log("Using mock data for development");
            setStats([
              { title: "Total Users", value: "1,250", icon: Users },
              { title: "Total Listings", value: "589", icon: Wheat },
              { title: "Total Orders", value: "324", icon: ShoppingCart },
              { title: "Revenue (FCFA)", value: "2,450,000 FCFA", icon: DollarSign },
            ]);
          }
          return;
        }

        const data = await res.json();
        console.log("API Data received:", data);

        // Update stats with real data
        setStats([
          { 
            title: "Total Users", 
            value: data.users ? data.users.toLocaleString() : "0", 
            icon: Users 
          },
          { 
            title: "Total Listings", 
            value: data.listings ? data.listings.toLocaleString() : "0", 
            icon: Wheat 
          },
          { 
            title: "Total Orders", 
            value: data.orders ? data.orders.toLocaleString() : "0", 
            icon: ShoppingCart 
          },
          {
            title: "Revenue (FCFA)",
            value: data.revenue 
              ? `${Number(data.revenue).toLocaleString("fr-FR")} FCFA` 
              : "0 FCFA",
            icon: DollarSign,
          },
        ]);
      } catch (err) {
        console.error("Error fetching admin stats:", err);
        // For development, use mock data
        if (process.env.NODE_ENV === "development") {
          setStats([
            { title: "Total Users", value: "1,250", icon: Users },
            { title: "Total Listings", value: "589", icon: Wheat },
            { title: "Total Orders", value: "324", icon: ShoppingCart },
            { title: "Revenue (FCFA)", value: "2,450,000 FCFA", icon: DollarSign },
          ]);
        }
      } finally {
        setIsFetching(false);
      }
    };

    fetchStats();
  }, [role, loading, router, logout]);

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-gray-600" />
          <div className="text-lg text-gray-600">Loading admin dashboard...</div>
        </div>
      </div>
    );
  }

  // Don't render if not admin (will redirect)
  if (role !== "admin") {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-gray-600" />
          <div className="text-lg text-gray-600">Redirecting...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Admin Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Admin Dashboard</h1>
        <p className="text-gray-600">Welcome back, Administrator</p>
      </div>

      {/* Stats Overview */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Overview Statistics</h2>
          <div className="flex items-center gap-4">
            {isFetching && (
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Loader2 className="w-4 h-4 animate-spin" />
                Updating stats...
              </div>
            )}
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => window.location.reload()}
              className="text-sm"
            >
              Refresh
            </Button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => (
            <Card key={stat.title} className="shadow-sm hover:shadow-md transition-shadow duration-200">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardDescription className="text-sm font-medium text-gray-600">
                  {stat.title}
                </CardDescription>
                <div className="p-2 bg-gray-100 rounded-full">
                  <stat.icon className="w-4 h-4 text-gray-600" />
                </div>
              </CardHeader>
              <CardContent>
                <CardTitle className="text-2xl font-bold">
                  {isFetching ? (
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Loading...
                    </div>
                  ) : (
                    stat.value
                  )}
                </CardTitle>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Quick Actions Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card className="shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Recent Activity</CardTitle>
            <CardDescription>Latest system activities</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">New user registration</p>
                  <p className="text-sm text-gray-500">2 minutes ago</p>
                </div>
                <Users className="w-5 h-5 text-gray-400" />
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">Order completed</p>
                  <p className="text-sm text-gray-500">15 minutes ago</p>
                </div>
                <ShoppingCart className="w-5 h-5 text-gray-400" />
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">New listing added</p>
                  <p className="text-sm text-gray-500">1 hour ago</p>
                </div>
                <Wheat className="w-5 h-5 text-gray-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Quick Actions</CardTitle>
            <CardDescription>Frequently used admin tasks</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3">
              <Button variant="outline" className="h-auto py-4 flex flex-col gap-2">
                <Users className="w-6 h-6" />
                <span>Manage Users</span>
              </Button>
              <Button variant="outline" className="h-auto py-4 flex flex-col gap-2">
                <Wheat className="w-6 h-6" />
                <span>View Listings</span>
              </Button>
              <Button variant="outline" className="h-auto py-4 flex flex-col gap-2">
                <ShoppingCart className="w-6 h-6" />
                <span>Process Orders</span>
              </Button>
              <Button variant="outline" className="h-auto py-4 flex flex-col gap-2">
                <DollarSign className="w-6 h-6" />
                <span>View Revenue</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminPage;