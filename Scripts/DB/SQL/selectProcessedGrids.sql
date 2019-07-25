CREATE OR REPLACE FUNCTION selectProcessedGrids(_mstrid integer)
RETURNS setof processedgrids language sql
AS
$$
   select *
   From processedgrids
   where mstrid = _mstrid;
$$;