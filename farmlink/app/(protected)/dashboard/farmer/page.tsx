"use client";

import React, { useEffect, useState } from "react";
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Package, 
  ShoppingCart, 
  DollarSign, 
  Plus, 
  Loader2,
  BarChart3,
  CheckCircle,
  Clock,
  AlertCircle
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import Link from "next/link";

const FarmerDashboard = () => {
  const { role, loading, logout } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState({
    totalListings: 0,
    activeOrders: 0,
    pendingOrders: 0,
    totalRevenue: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (loading) return;

    if (role !== "farmer") {
      router.push("/dashboard");
      return;
    }

    fetchFarmerStats();
  }, [role, loading, router]);

  const fetchFarmerStats = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/farmer/stats", {
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        setStats({
          totalListings: data.totalListings || 0,
          activeOrders: data.activeOrders || 0,
          pendingOrders: data.pendingOrders || 0,
          totalRevenue: data.totalRevenue || 0,
        });
      }
    } catch (error) {
      console.error("Error fetching farmer stats:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (loading || role !== "farmer") {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Farmer Dashboard</h1>
          <p className="text-gray-600">Manage your crop listings and orders</p>
        </div>
        <div className="flex gap-3">
          <Button asChild>
            <Link href="/dashboard/farmer/listings/new">
              <Plus className="w-4 h-4 mr-2" />
              New Listing
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/dashboard/farmer/orders">
              View Orders
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Total Listings
            </CardTitle>
            <Package className="w-5 h-5 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                stats.totalListings
              )}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Active crop listings
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Pending Orders
            </CardTitle>
            <Clock className="w-5 h-5 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                stats.pendingOrders
              )}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Awaiting confirmation
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Active Orders
            </CardTitle>
            <ShoppingCart className="w-5 h-5 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                stats.activeOrders
              )}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              In progress
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Total Revenue
            </CardTitle>
            <DollarSign className="w-5 h-5 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                `FCFA ${stats.totalRevenue.toLocaleString()}`
              )}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Lifetime earnings
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="w-5 h-5" />
              Quick Actions
            </CardTitle>
            <CardDescription>Manage your farming business</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full justify-start" asChild>
              <Link href="/dashboard/farmer/listings/new">
                <Plus className="w-4 h-4 mr-2" />
                Create New Listing
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link href="/dashboard/farmer/listings">
                <Package className="w-4 h-4 mr-2" />
                Manage Listings
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link href="/dashboard/farmer/orders">
                <ShoppingCart className="w-4 h-4 mr-2" />
                View All Orders
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link href="/dashboard/farmer/analytics">
                <BarChart3 className="w-4 h-4 mr-2" />
                View Analytics
              </Link>
            </Button>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              Recent Activity
            </CardTitle>
            <CardDescription>Latest updates on your farm</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">New order received</p>
                  <p className="text-sm text-gray-500">Maize - 100kg</p>
                </div>
                <div className="text-sm text-gray-500">10 min ago</div>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">Listing updated</p>
                  <p className="text-sm text-gray-500">Rice quantity increased</p>
                </div>
                <div className="text-sm text-gray-500">2 hours ago</div>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">Payment confirmed</p>
                  <p className="text-sm text-gray-500">Order #ORD-789</p>
                </div>
                <CheckCircle className="w-5 h-5 text-green-500" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tips & Resources */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Farming Tips</CardTitle>
          <CardDescription>Best practices for successful farming</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold mb-2">Seasonal Planning</h3>
              <p className="text-sm text-gray-600">
                Plan your crop rotations according to seasons for optimal yield.
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold mb-2">Pricing Strategy</h3>
              <p className="text-sm text-gray-600">
                Set competitive prices based on market trends and quality.
              </p>
            </div>
            <div className="p-4 bg-yellow-50 rounded-lg">
              <h3 className="font-semibold mb-2">Quality Control</h3>
              <p className="text-sm text-gray-600">
                Maintain high quality standards to build customer trust.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FarmerDashboard;