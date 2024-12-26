def count_cart(cart):
    total_amount, total_quantiy = 0, 0

    if cart:
        for c in cart.values():
            total_quantiy += c['quantity']
            if c['is_selected']:
                total_amount += c['quantity']*c['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantiy,
        "books": cart
    }