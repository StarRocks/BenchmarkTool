--Q11
select count(*) from (select count(*) from lineorder_flat  group by lo_shipmode,lo_orderpriority,p_category,s_nation,c_nation,p_mfgr) t;
