CREATE OR REPLACE FUNCTION selectCoastData(_ogc_fid integer)
RETURNS setof cp_coast_la language sql
AS
$$
   select *
   From cp_coast_la
   where _ogc_fid = _ogc_fid;
$$;