-- Crear un procedimiento almacenado para obtener detalles de un pedido en el esquema "ecommerce"
CREATE OR REPLACE PROCEDURE ecommerce.GetOrderDetails(IN p_order_id INT)
LANGUAGE SQL
AS $$
BEGIN
    -- Seleccionar información del pedido
    SELECT * FROM ecommerce.orders WHERE order_id = p_order_id INTO OUTER order_info;

    -- Seleccionar detalles del pedido, incluyendo productos asociados
    SELECT
        od.order_detail_id,
        od.product_id,
        p.product_name,
        od.quantity,
        od.unit_price,
        od.subtotal
    FROM
        ecommerce.order_details od
    INNER JOIN
        ecommerce.products p ON od.product_id = p.product_id
    WHERE
        od.order_id = p_order_id
    INTO
        OUTER order_details;

    -- Devolver los resultados
    RETURN QUERY
    SELECT
        order_info.*,
        order_details.order_detail_id,
        order_details.product_id,
        order_details.product_name,
        order_details.quantity,
        order_details.unit_price,
        order_details.subtotal;
END;
$$;
