import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  console.log("✅ Admin stats API route hit!");
  
  try {
    // Get token from cookies
    const token = request.cookies.get("access_token")?.value;
    
    if (!token) {
      console.log("No access token found in cookies");
      return NextResponse.json(
        { error: "No authorization token found" },
        { status: 401 }
      );
    }

    // CORRECTED: Use the right backend URL and endpoint
    const backendUrl = process.env.BACKEND_URL || "http://127.0.0.1:8003";
    const backendEndpoint = `${backendUrl}/api/v1/analytics/stats`;
    
    console.log("Forwarding to backend:", backendEndpoint);
    
    const response = await fetch(backendEndpoint, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
    });

    console.log("Backend response status:", response.status);

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { detail: `Backend error: ${response.status} ${response.statusText}` };
      }
      
      console.error("Backend error:", response.status, errorData);
      
      // For development, return mock data if backend fails
      console.log("Returning mock data as fallback");
      return NextResponse.json({ 
        users: 1250,
        listings: 589,
        orders: 324,
        revenue: 2450000,
        message: "Mock data - Backend endpoint failed"
      });
    }

    const data = await response.json();
    console.log("✅ Backend data received:", data);
    
    return NextResponse.json(data);

  } catch (error) {
    console.error("Error in admin stats API:", error);
    
    // Return mock data if connection fails
    console.log("Returning mock data due to connection error");
    return NextResponse.json({ 
      users: 1250,
      listings: 589,
      orders: 324,
      revenue: 2450000,
      message: "Mock data - Connection error"
    });
  }
}