export type OrderStatus = 'pending' | 'preparing' | 'ready' | 'completed' | 'cancelled'

export interface OrderType {
    id: string
    dish_name: string
    quantity: number
    status: OrderStatus
    special_instructions?: string
    created_at: string
    updated_at?: string
}

export interface OrderCreateInput {
    dish_name: string
    quantity: number
    special_instructions?: string
}

export interface OrderUpdateInput {
    status: OrderStatus
    special_instructions?: string
}