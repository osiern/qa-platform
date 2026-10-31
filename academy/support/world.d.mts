export const baseURL: string;
export interface Product {
    id: number;
    name: string;
    price: number;
    stock: number;
}
export interface World {
    user: { email: string; password: string };
    product: Product;
    products: Product[];
    searchPrefix: string;
    cleanup(extraToken?: string | null): Promise<void>;
}
export function createWorld(options?: { productCount?: number }): Promise<World>;
