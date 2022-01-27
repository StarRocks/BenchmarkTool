--Q8
select count(*) from lineorder_flat group by lo_orderdate,s_nation,s_region;
