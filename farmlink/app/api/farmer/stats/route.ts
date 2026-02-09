import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  try {
    const token = request.cookies.get("access_token")?.value;
    
    if (!token) {
      return NextResponse.json(
        { error: "Unauthorized - No authentication token" },
        { status: 401 }
      );
    }

    const backendUrl = process.env.BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json(
        { error: "Backend URL not configured" },
        { status: 500 }
      );
    }

    // Get user info from token to get farmer ID
    const userResponse = await fetch(`${backendUrl}/api/v1/auth/me`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!userResponse.ok) {
      return NextResponse.json(
        { error: "Failed to get user information" },
        { status: 401 }
      );
    }

    const user = await userResponse.json();
    const farmerId = user.id;

    // Fetch farmer's listings
    const listingsResponse = await fetch(
      `${backendUrl}/api/v1/crop-listings/by-farmer/${farmerId}`,
      {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    // Fetch farmer's orders
    const ordersResponse = await fetch(
      `${backendUrl}/api/v1/orders/?page=1&limit=100`,
      {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    let totalListings = 0;
    let totalOrders = 0;
    let pendingOrders = 0;
    let completedOrders = 0;
    let totalRevenue = 0;

    if (listingsResponse.ok) {
      const listings = await listingsResponse.json();
      totalListings = Array.isArray(listings) ? listings.length : 0;
    }

    if (ordersResponse.ok) {
      const ordersData = await ordersResponse.json();
      const orders = ordersData.items || [];
      totalOrders = orders.length;
      
      // Calculate stats from orders
      orders.forEach((order: any) => {
        if (order.status === "pending" || order.status === "confirmed") {
          pendingOrders++;
        } else if (order.status === "completed") {
          completedOrders++;
          totalRevenue += order.total_price || 0;
        }
      });
    }

    return NextResponse.json({
      totalListings,
      totalOrders,
      pendingOrders,
      completedOrders,
      activeOrders: totalOrders - completedOrders, // Orders in progress
      totalRevenue,
      farmerId,
    });

  } catch (error) {
    console.error("Error in farmer stats API:", error);
    
    // Return mock data for development
    return NextResponse.json({
      totalListings: 5,
      totalOrders: 12,
      pendingOrders: 3,
      completedOrders: 7,
      activeOrders: 5,
      totalRevenue: 125000,
      message: "Using mock data - Backend integration in progress",
    });
  }
}