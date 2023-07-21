INSERT INTO 
    attributed_checkouts
    SELECT
        checkout_id,
        username as user_name,
        click_id,
        product_id,
        payment_method,
        total_amount,
        shipping_address,
        billing_address,
        user_agent,
        ip_address,
        checkout_time,
        click_time
    FROM
        (
            SELECT
            co.checkout_id,
            u.username,
            c1.click_id,
            co.product_id,
            co.payment_method,
            co.total_amount,
            co.shipping_address,
            co.billing_address,
            co.user_agent,
            co.ip_address,
            co.datetime_occured as checkout_time,
            c1.datetime_occured as click_time,
            ROW_NUMBER() OVER( PARTITION BY
                c1.user_id, c1.product_id
                ORDER BY
                c1.datetime_occured
            ) as click_order

            FROM
                checkouts as co
                JOIN users FOR SYSTEM_TIME AS OF co.processing_time AS u ON co.user_id = u.id
                LEFT JOIN clicks as c1 on c1.user_id = co.user_id
                AND c1.product_id = co.product_id
                AND co.datetime_occured BETWEEN c1.datetime_occured
                and c1.datetime_occured + INTERVAL '1' HOUR
        ) as subquery

    WHERE click_order = 1 ;
