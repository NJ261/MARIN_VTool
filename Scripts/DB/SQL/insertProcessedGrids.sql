create procedure insertProcessedGrids(IN _id integer, IN _mstrid numeric, IN _grid0_1 numeric, IN _geom geometry)
language plpgsql
as $$begin
        insert into processedgrids(id, mstrid, grid0_1, geom) values (_id, _mstrid, _grid0_1, _geom);
    end;
$$;