export type CartItem = {
  slug: string;
  name: string;
  price_cents: number;
  quantity: number;
};

const KEY = "rackside.cart.v1";

function isValid(item: unknown): item is CartItem {
  const entry = item as Partial<CartItem>;
  return (
    typeof entry?.slug === "string" &&
    typeof entry?.name === "string" &&
    Number.isFinite(entry?.price_cents) &&
    Number.isFinite(entry?.quantity) &&
    (entry.quantity as number) > 0
  );
}

export function getCart(): CartItem[] {
  try {
    const raw = localStorage.getItem(KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed.filter(isValid) : [];
  } catch {
    return [];
  }
}

function save(items: CartItem[]): void {
  localStorage.setItem(KEY, JSON.stringify(items));
  window.dispatchEvent(new CustomEvent("cart:change"));
}

export function addItem(item: Omit<CartItem, "quantity">): void {
  const items = getCart();
  const existing = items.find((entry) => entry.slug === item.slug);
  if (existing) {
    existing.quantity += 1;
  } else {
    items.push({ ...item, quantity: 1 });
  }
  save(items);
}

export function setQuantity(slug: string, quantity: number): void {
  let items = getCart();
  if (quantity <= 0) {
    items = items.filter((entry) => entry.slug !== slug);
  } else {
    items = items.map((entry) =>
      entry.slug === slug ? { ...entry, quantity } : entry,
    );
  }
  save(items);
}

export function removeItem(slug: string): void {
  save(getCart().filter((entry) => entry.slug !== slug));
}

export function clearCart(): void {
  save([]);
}

export function cartCount(): number {
  return getCart().reduce((sum, item) => sum + item.quantity, 0);
}

export function cartTotal(): number {
  return getCart().reduce(
    (sum, item) => sum + item.price_cents * item.quantity,
    0,
  );
}
