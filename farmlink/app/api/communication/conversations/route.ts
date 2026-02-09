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

    const response = await fetch(`${backendUrl}/api/v1/communication/conversations`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || `Failed to fetch conversations: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error("Error in conversations API:", error);
    
    // Return mock data for development
    return NextResponse.json([
      {
        id: "1",
        other_user_id: "user-123",
        other_user_name: "Buyer John",
        other_user_role: "buyer",
        last_message: "When can you deliver the maize?",
        last_message_at: "2024-01-15T10:30:00Z",
        unread_count: 2,
      },
      {
        id: "2",
        other_user_id: "user-456",
        other_user_name: "Buyer Sarah",
        other_user_role: "buyer",
        last_message: "The rice quality was excellent!",
        last_message_at: "2024-01-14T14:20:00Z",
        unread_count: 0,
      },
      {
        id: "3",
        other_user_id: "user-789",
        other_user_name: "Buyer Mike",
        other_user_role: "buyer",
        last_message: "Do you have more tomatoes available?",
        last_message_at: "2024-01-13T09:15:00Z",
        unread_count: 1,
      },
    ]);
  }
}