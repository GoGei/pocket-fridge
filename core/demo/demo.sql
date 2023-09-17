CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DELETE
FROM fridge_product;
DELETE
FROM fridge;
DELETE
FROM fridge_type;
UPDATE users
SET is_active = False
WHERE email = 'rich.290401@gmail.com';


-- User interactions
SELECT id, is_active, email, created_stamp, password
FROM users
WHERE email = 'rich.290401@gmail.com';

UPDATE users
SET is_active = True
WHERE email = 'rich.290401@gmail.com';

-- Check user
SELECT id, is_active, email, created_stamp, password
FROM users
WHERE email = 'rich.290401@gmail.com';

-- Fridge type interactions
INSERT INTO fridge_type (name, slug, created_stamp, modified_stamp)
VALUES ('Fridge', 'fridge', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Freezer', 'freezer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Pantry', 'pantry', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
       ('Some long name', 'some-long-name', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Fridge type check
SELECT id, name, slug
FROM fridge_type;

DO
$$
    DECLARE
        my_fridge_type_id INT;
        my_storage_id     UUID;
    BEGIN
        INSERT INTO fridge_type (name, slug, created_stamp, modified_stamp)
        VALUES ('Test', 'test', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT (slug) DO UPDATE
            SET slug = excluded.slug
        RETURNING id INTO my_fridge_type_id;

        -- Fridge
        INSERT INTO fridge (id, name, user_id, fridge_type_id, created_stamp, modified_stamp)
        VALUES (uuid_generate_v4(), 'Fridge 1', 1, my_fridge_type_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        RETURNING id INTO my_storage_id;

        -- Products
        INSERT INTO fridge_product (id, name, storage_id, amount, units, manufacture_date, shelf_life_date, notes,
                                    image, barcode, created_stamp, modified_stamp)
        VALUES (uuid_generate_v4(), 'Fridge Product 1', my_storage_id, 2.5, 'kilogram', CURRENT_DATE, CURRENT_DATE,
                'Some notes', null, null, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


    END;
$$;

-- Select data
SELECT fridge_product.name, fridge_product.amount, fridge_product.units, fridge.name AS fridge_name, users.email
FROM fridge_product
         INNER JOIN fridge ON (fridge_product.storage_id = fridge.id)
         INNER JOIN users ON (fridge.user_id = users.id)
WHERE users.email = 'rich.290401@gmail.com';