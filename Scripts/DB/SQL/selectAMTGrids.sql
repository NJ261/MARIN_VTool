CREATE OR REPLACE FUNCTION selectAMTGrids(_mstrid integer)
RETURNS setof amtgrids language sql
AS
$$
   select *
   From amtgrids
   where mstrid = _mstrid;
$$;