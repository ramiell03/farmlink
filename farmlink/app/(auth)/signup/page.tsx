"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Link from "next/link";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export default function SignUpPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "buyer", // Default role
    location: "",
    phone_number: "",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSignUp = async () => {
    // Basic validation
    if (formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    // Additional validation for farmers and buyers
    if (formData.role === "farmer" || formData.role === "buyer") {
      if (!formData.location.trim()) {
        toast.error("Location is required for farmers and buyers");
        return;
      }
      if (!formData.phone_number.trim()) {
        toast.error("Phone number is required for farmers and buyers");
        return;
      }
    }

    // Admin users don't need location and phone
    if (formData.role === "admin") {
      formData.location = "";
      formData.phone_number = "";
    }

    const id = toast.loading("Creating account...");
    setIsLoading(true);

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          role: formData.role,
          location: formData.location || null,
          phone_number: formData.phone_number || null,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || data.detail || "Failed to register");
      }

      toast.success("Account created successfully!", { id });
      
      // Redirect to login page after successful registration
      setTimeout(() => {
        router.push("/signin");
      }, 1500);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Failed to create account";
      toast.error(message, { id });
    } finally {
      setIsLoading(false);
    }
  };

  const isFarmerOrBuyer = formData.role === "farmer" || formData.role === "buyer";

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Create an account</CardTitle>
        <CardDescription>
          Enter your details to create a new account
        </CardDescription>
      </CardHeader>

      <CardContent className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="username">Full name</Label>
          <Input
            id="username"
            placeholder="John Doe"
            value={formData.username}
            onChange={(e) => handleInputChange("username", e.target.value)}
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="john@example.com"
            value={formData.email}
            onChange={(e) => handleInputChange("email", e.target.value)}
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="role">Account Type</Label>
          <Select
            value={formData.role}
            onValueChange={(value) => handleInputChange("role", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="buyer">Buyer</SelectItem>
              <SelectItem value="farmer">Farmer</SelectItem>
            </SelectContent>
          </Select>
          <p className="text-xs text-muted-foreground">
            {formData.role === "admin" 
              ? "Admin accounts have full system access"
              : "Farmers and buyers need location and phone number"
            }
          </p>
        </div>

        <div className="grid gap-2">
          <Label htmlFor="location">
            Location {isFarmerOrBuyer && <span className="text-red-500">*</span>}
          </Label>
          <Input
            id="location"
            placeholder="City, Country"
            value={formData.location}
            onChange={(e) => handleInputChange("location", e.target.value)}
            required={isFarmerOrBuyer}
          />
          {isFarmerOrBuyer && (
            <p className="text-xs text-muted-foreground">
              Required for {formData.role}s
            </p>
          )}
        </div>

        <div className="grid gap-2">
          <Label htmlFor="phone_number">
            Phone Number {isFarmerOrBuyer && <span className="text-red-500">*</span>}
          </Label>
          <Input
            id="phone_number"
            type="tel"
            placeholder="+1234567890"
            value={formData.phone_number}
            onChange={(e) => handleInputChange("phone_number", e.target.value)}
            required={isFarmerOrBuyer}
          />
          {isFarmerOrBuyer && (
            <p className="text-xs text-muted-foreground">
              Required for {formData.role}s
            </p>
          )}
        </div>

        <div className="grid gap-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => handleInputChange("password", e.target.value)}
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="confirmPassword">Confirm Password</Label>
          <Input
            id="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={(e) => handleInputChange("confirmPassword", e.target.value)}
          />
        </div>

        <Button 
          onClick={handleSignUp} 
          className="w-full"
          disabled={isLoading}
        >
          {isLoading ? "Creating account..." : "Sign up"}
        </Button>
      </CardContent>

      <CardFooter className="flex flex-col gap-2">
        <p className="text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/signin" className="underline">
            Sign in
          </Link>
        </p>
        <p className="text-xs text-muted-foreground">
          By signing up, you agree to our Terms of Service and Privacy Policy
        </p>
      </CardFooter>
    </Card>
  );
}