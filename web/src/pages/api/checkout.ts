import type { APIRoute } from "astro";
import { createCheckout } from "@/lib/api";

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json().catch(() => null);
  const items = body?.items;
  if (!Array.isArray(items) || items.length === 0) {
    return Response.json({ error: "Cart is empty" }, { status: 400 });
  }

  const url = await createCheckout(items);
  if (!url) {
    return Response.json({ error: "Checkout failed" }, { status: 502 });
  }
  return Response.json({ url });
};
