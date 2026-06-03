export type Product = {
  id: string;
  slug: string;
  name: string;
  description: string;
  price_cents: number;
  image_url: string | null;
  category: string;
  stock: number;
  active: boolean;
};

export type OrderItem = {
  name: string;
  price_cents: number;
  quantity: number;
};

export type Order = {
  id: string;
  email: string;
  amount_cents: number;
  status: string;
  created_at: string;
  items: OrderItem[];
};
