--Q5
select count(*),lo_shipmode,s_city from lineorder_flat group by lo_shipmode,s_city;
