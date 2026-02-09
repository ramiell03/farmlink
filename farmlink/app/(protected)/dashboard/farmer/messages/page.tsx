"use client";

import React, { useEffect, useState, useRef } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  MessageSquare,
  Search,
  Send,
  Loader2,
  Users,
  Clock,
  Check,
  CheckCheck,
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

interface Conversation {
  id: string;
  other_user_id: string;
  other_user_name: string;
  other_user_role: string;
  last_message: string;
  last_message_at: string;
  unread_count: number;
}

interface Message {
  id: string;
  sender_id: string;
  receiver_id: string;
  content: string;
  created_at: string;
  read?: boolean;
}

const FarmerMessagesPage = () => {
  const { role, loading } = useAuth();
  const router = useRouter();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (loading) return;

    if (role !== "farmer") {
      router.push("/dashboard");
      return;
    }

    fetchConversations();
  }, [role, loading, router]);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages(selectedConversation.other_user_id);
    }
  }, [selectedConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchConversations = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/communication/conversations", {
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        setConversations(data);
        if (data.length > 0 && !selectedConversation) {
          setSelectedConversation(data[0]);
        }
      }
    } catch (error) {
      console.error("Error fetching conversations:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchMessages = async (userId: string) => {
    try {
      const response = await fetch(`/api/communication/messages/${userId}`, {
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      }
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedConversation || isSending) return;

    setIsSending(true);
    const tempId = `temp-${Date.now()}`;
    const tempMessage: Message = {
      id: tempId,
      sender_id: "current-user",
      receiver_id: selectedConversation.other_user_id,
      content: newMessage,
      created_at: new Date().toISOString(),
      read: false,
    };

    setMessages([...messages, tempMessage]);
    const messageToSend = newMessage;
    setNewMessage("");

    try {
      const response = await fetch(`/api/communication/messages/${selectedConversation.other_user_id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: 'include',
        body: JSON.stringify({ content: messageToSend }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }

      const data = await response.json();
      
      // Replace temp message with real one
      setMessages(prev => prev.map(msg => 
        msg.id === tempId ? { ...data.message, id: data.message.id } : msg
      ));

      // Update conversation list
      setConversations(prev => prev.map(conv => 
        conv.other_user_id === selectedConversation.other_user_id
          ? {
              ...conv,
              last_message: messageToSend,
              last_message_at: new Date().toISOString(),
            }
          : conv
      ));

    } catch (error) {
      console.error("Error sending message:", error);
      // Remove temp message on error
      setMessages(prev => prev.filter(msg => msg.id !== tempId));
      setNewMessage(messageToSend);
    } finally {
      setIsSending(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const formatTime = (dateString: string) => {
    return format(new Date(dateString), "hh:mm a");
  };

  const formatDate = (dateString: string) => {
    return format(new Date(dateString), "MMM d, yyyy");
  };

  const filteredConversations = conversations.filter(conv =>
    conv.other_user_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Messages</h1>
        <p className="text-gray-600">Communicate with buyers and manage inquiries</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-200px)]">
        {/* Conversations List */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Conversations</CardTitle>
              <Badge variant="outline" className="bg-blue-50 text-blue-700">
                <Users className="w-3 h-3 mr-1" />
                {conversations.length}
              </Badge>
            </div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                placeholder="Search conversations..."
                className="pl-10"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </CardHeader>
          <CardContent className="p-0">
            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
              </div>
            ) : filteredConversations.length === 0 ? (
              <div className="text-center py-12">
                <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No conversations yet
                </h3>
                <p className="text-gray-500">
                  Start chatting with buyers who inquire about your crops.
                </p>
              </div>
            ) : (
              <div className="divide-y">
                {filteredConversations.map((conversation) => (
                  <button
                    key={conversation.id}
                    className={cn(
                      "w-full p-4 text-left hover:bg-gray-50 transition-colors",
                      selectedConversation?.id === conversation.id && "bg-blue-50"
                    )}
                    onClick={() => setSelectedConversation(conversation)}
                  >
                    <div className="flex items-start gap-3">
                      <Avatar>
                        <AvatarFallback className="bg-blue-100 text-blue-600">
                          {conversation.other_user_name.charAt(0)}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <div className="flex justify-between items-start mb-1">
                          <h4 className="font-semibold truncate">
                            {conversation.other_user_name}
                          </h4>
                          <span className="text-xs text-gray-500 whitespace-nowrap">
                            {formatTime(conversation.last_message_at)}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 truncate mb-1">
                          {conversation.last_message}
                        </p>
                        <div className="flex justify-between items-center">
                          <Badge
                            variant="outline"
                            className="text-xs bg-gray-100"
                          >
                            {conversation.other_user_role}
                          </Badge>
                          {conversation.unread_count > 0 && (
                            <Badge className="bg-blue-600 text-white">
                              {conversation.unread_count}
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Chat Area */}
        <Card className="lg:col-span-2 flex flex-col">
          {selectedConversation ? (
            <>
              <CardHeader className="border-b">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Avatar>
                      <AvatarFallback className="bg-blue-100 text-blue-600">
                        {selectedConversation.other_user_name.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <CardTitle>{selectedConversation.other_user_name}</CardTitle>
                      <CardDescription className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs">
                          {selectedConversation.other_user_role}
                        </Badge>
                        <span className="flex items-center text-xs">
                          <Clock className="w-3 h-3 mr-1" />
                          Last active recently
                        </span>
                      </CardDescription>
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    View Profile
                  </Button>
                </div>
              </CardHeader>

              <CardContent className="flex-1 overflow-y-auto p-0">
                <div className="p-6 space-y-4">
                  {messages.length === 0 ? (
                    <div className="text-center py-12">
                      <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Start a conversation
                      </h3>
                      <p className="text-gray-500">
                        Send your first message to {selectedConversation.other_user_name}
                      </p>
                    </div>
                  ) : (
                    <>
                      {messages.map((message, index) => {
                        const isCurrentUser = message.sender_id === "current-user";
                        const showDate = index === 0 || 
                          formatDate(messages[index - 1].created_at) !== formatDate(message.created_at);
                        
                        return (
                          <React.Fragment key={message.id}>
                            {showDate && (
                              <div className="flex justify-center my-4">
                                <Badge variant="secondary" className="text-xs">
                                  {formatDate(message.created_at)}
                                </Badge>
                              </div>
                            )}
                            <div
                              className={cn(
                                "flex",
                                isCurrentUser ? "justify-end" : "justify-start"
                              )}
                            >
                              <div
                                className={cn(
                                  "max-w-[70%] rounded-lg px-4 py-2",
                                  isCurrentUser
                                    ? "bg-blue-600 text-white rounded-br-none"
                                    : "bg-gray-100 text-gray-900 rounded-bl-none"
                                )}
                              >
                                <p className="text-sm">{message.content}</p>
                                <div
                                  className={cn(
                                    "flex items-center justify-end gap-1 mt-1 text-xs",
                                    isCurrentUser ? "text-blue-200" : "text-gray-500"
                                  )}
                                >
                                  <span>{formatTime(message.created_at)}</span>
                                  {isCurrentUser && (
                                    message.read ? (
                                      <CheckCheck className="w-3 h-3" />
                                    ) : (
                                      <Check className="w-3 h-3" />
                                    )
                                  )}
                                </div>
                              </div>
                            </div>
                          </React.Fragment>
                        );
                      })}
                      <div ref={messagesEndRef} />
                    </>
                  )}
                </div>
              </CardContent>

              <div className="border-t p-4">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    sendMessage();
                  }}
                  className="flex gap-2"
                >
                  <Input
                    placeholder="Type your message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                      }
                    }}
                    disabled={isSending}
                    className="flex-1"
                  />
                  <Button type="submit" disabled={isSending || !newMessage.trim()}>
                    {isSending ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Send className="w-4 h-4" />
                    )}
                  </Button>
                </form>
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-12">
              <MessageSquare className="w-16 h-16 text-gray-300 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Select a conversation
              </h3>
              <p className="text-gray-500 text-center max-w-md">
                Choose a conversation from the list to start messaging with buyers
                or view your message history.
              </p>
            </div>
          )}
        </Card>
      </div>

      {/* Tips Section */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Communication Tips</CardTitle>
          <CardDescription>Best practices for effective communication with buyers</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold mb-2">Respond Promptly</h3>
              <p className="text-sm text-gray-600">
                Quick responses increase buyer confidence and lead to faster sales.
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold mb-2">Be Professional</h3>
              <p className="text-sm text-gray-600">
                Use clear language and maintain a professional tone in all communications.
              </p>
            </div>
            <div className="p-4 bg-yellow-50 rounded-lg">
              <h3 className="font-semibold mb-2">Provide Details</h3>
              <p className="text-sm text-gray-600">
                Include crop quality, delivery options, and payment terms in your messages.
              </p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <h3 className="font-semibold mb-2">Follow Up</h3>
              <p className="text-sm text-gray-600">
                Follow up on inquiries and keep buyers updated on order status.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FarmerMessagesPage;