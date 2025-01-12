'use client'

import { useState } from 'react'
import { Form, Input, InputNumber, Button, Card, message } from 'antd'
import { ShoppingCartOutlined } from '@ant-design/icons'

interface OrderForm {
    dishName: string
    quantity: number
}

export default function OrderPage() {
    const [form] = Form.useForm()
    const [loading, setLoading] = useState(false)
    const [messageApi, contextHolder] = message.useMessage()

    const onFinish = async (values: OrderForm) => {
        setLoading(true)
        try {
            const response = await fetch('http://localhost:8000/api/v1/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    dish_name: values.dishName,
                    quantity: values.quantity,
                }),
            })

            if (response.ok) {
                messageApi.success('Order placed successfully')
                form.resetFields()
            } else {
                throw new Error('Failed to place order')
            }
        } catch {
            messageApi.error('Failed to place order. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{
            minHeight: '100vh',
            padding: '2rem',
            background: '#f5f5f5',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'flex-start'
        }}>
            {contextHolder}
            <Card
                title="Place Your Order"
                style={{ maxWidth: 600, width: '100%' }}
                extra={<ShoppingCartOutlined style={{ fontSize: '24px' }} />}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={onFinish}
                    initialValues={{ quantity: 1 }}
                >
                    <Form.Item
                        label="Dish Name"
                        name="dishName"
                        rules={[
                            { required: true, message: 'Please enter the dish name' },
                            { min: 2, message: 'Dish name must be at least 2 characters' }
                        ]}
                    >
                        <Input placeholder="Enter dish name" size="large" />
                    </Form.Item>

                    <Form.Item
                        label="Quantity"
                        name="quantity"
                        rules={[
                            { required: true, message: 'Please enter the quantity' },
                            { type: 'number', min: 1, message: 'Quantity must be at least 1' }
                        ]}
                    >
                        <InputNumber
                            min={1}
                            placeholder="Enter quantity"
                            size="large"
                            style={{ width: '100%' }}
                        />
                    </Form.Item>

                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            loading={loading}
                            size="large"
                            block
                        >
                            Place Order
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
        </div>
    )
}