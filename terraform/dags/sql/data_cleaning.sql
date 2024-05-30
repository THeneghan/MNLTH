-- Data Cleaning
DELETE FROM credit_cards
WHERE id IN
    (SELECT id
    FROM
        (SELECT id,
         ROW_NUMBER() OVER( PARTITION BY "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14",
             "V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount","Class"
        ORDER BY  id ) AS row_num
        FROM credit_cards ) t
        WHERE t.row_num > 1 );



create or replace view normalised_data as
select "id",
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14",
             "V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28",
    ("Amount" - avg("Amount") over())/ STDDEV("Amount") over() as "Amount"
from credit_cards;






