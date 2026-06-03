import type { APIRoute } from "astro";
import { deleteProduct } from "@/lib/api";
import { getToken } from "@/lib/auth";

export const POST: APIRoute = async ({ cookies, redirect, params }) => {
  const token = getToken(cookies);
  if (!token) {
    return redirect("/admin/login", 303);
  }

  await deleteProduct(token, params.id!);
  return redirect("/admin", 303);
};
