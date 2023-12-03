CREATE OR REPLACE PROCEDURE make_sale(
    customer_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10, 2)
)
AS
$$
DECLARE
    subtotal DECIMAL(10, 2);
BEGIN
    INSERT INTO orders (customer_id, order_date, status, total_amount)
    VALUES (customer_id, CURRENT_TIMESTAMP, 'Completed', 0)
    RETURNING order_id INTO order_id;

    INSERT INTO order_details (order_id, product_id, quantity, unit_price, subtotal)
    VALUES (order_id, product_id, quantity, unit_price, unit_price * quantity);

    UPDATE orders
    SET total_amount = (SELECT SUM(subtotal) FROM order_details WHERE order_id = order_id)
    WHERE order_id = order_id;

    UPDATE products
    SET stock_quantity = stock_quantity - quantity
    WHERE product_id = product_id;
END;
$$ LANGUAGE plpgsql;
