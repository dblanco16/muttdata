# Estructuras tablas

Tabla: USERS
Campos: 

EVENT_DATE (datetime)
USER_ID (string) *
EVENT_ID (int)
EVENT_VALUE (float)

donde EVENT_VALUE es:
EVENT_ID = 1 -> LOGIN
EVENT_ID = 2 -> PURCHASE
EVENT_ID = 3 -> REGISTER
EVENT_ID = 4 -> SHARE

Tabla: USERS_TPU 
(the top 5% of users who have made the highest quantity (not amount!) of purchases, during the period of a month)

Campos:

USER_ID (string) *
month (int)
year (int)
PURCHASE (int)

* PK

# 0. Carga tabla USERS_TPU

# periodo que se quiere generar
SET @periodo_mes := 1;
SET @periodo_anio := 2019;

# cantidad de usuario que compran en un mes determinado
SET @cant_users := (
    SELECT count(*)
    FROM USERS
    WHERE USERS.event_id = 2
    AND year(USERS.EVENT_DATE) = @periodo_anio
    AND month(USERS.EVENT_DATE) = @periodo_mes
    GROUP BY USERS.user_id
);

SET @cant_5porc :=  (@cant_users * 5) / 100;

INSERT INTO USERS_TPU(user_id, month, year, purchase)
SELECT USERS.user_id
,   @periodo_mes
,   @periodo_anio
,   count(*)
FROM USERS
WHERE USERS.event_id = 2
AND year(USERS.EVENT_DATE) = @periodo_anio
AND month(USERS.EVENT_DATE) = @periodo_mes
GROUP BY USERS.user_id
ORDER BY count(*) desc
LIMIT 0, @cant_5porc;

# Se asume un motor "standard" sql, otra sintaxis posible podria ser "TOP @cant_5porc", etc.

# 1. Count of UNIQUE USER_ID’s in the TPU (top 5% of purchasers, by quantity) group.

SELECT count(*)
FROM USERS_TPU
GROUP by USERS_TPU.user_id;

# 2.Average amount of purchases for each Top Performing User (TPU) for that month.

SELECT USERS_TPU.user_id
,   (USERS_TPU.PURCHASE) / 30 as PURCHASE_avg
FROM USERS_TPU
WHERE year(USERS_TPU.year) = @periodo_anio
AND month(USERS_TPU.month) = @periodo_mes;

# se generaliza con meses de 30 dias, otra opción es obtener la cantidad de dias del mes
# segun mes y año solicitado.

# 3.For each TPU, calculate the average amount of time between each pair of successive purchases. 
# We call this the Time Delta between purchases.

SELECT subquery.user_id
, avg(subquery.Time_Delta_purchases)
(
    SELECT USERS.user_id
    ,   ( (
            SELECT u.EVENT_DATE
            FROM USERS u
            WHERE u.user_id = USERS.user_id
            AND USERS.event_id = 2
            AND year(USERS.EVENT_DATE) = @periodo_anio
            AND month(USERS.EVENT_DATE) = @periodo_mes     
            AND u.EVENT_DATE > USERS.EVENT_DATE
            ORDER BY u.EVENT_DATE
            LIMIT 0, 1
        ) - USERS.EVENT_DATE
    ) as Time_Delta_purchases
    FROM USERS
    WHERE USERS.event_id = 2
    AND year(USERS.EVENT_DATE) = @periodo_anio
    AND month(USERS.EVENT_DATE) = @periodo_mes
) as subquery
GROUP BY subquery.user_id;
