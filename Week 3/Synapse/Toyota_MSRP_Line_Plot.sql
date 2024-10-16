SELECT
    Make,
    Year,
    MSRP
FROM
    OPENROWSET(
        BULK 'https://carretaildatalake.dfs.core.windows.net/db-csv-dwh/data.csv',
        FORMAT = 'CSV',
        PARSER_VERSION = '2.0',
        FIRSTROW = 2
    ) WITH (
        Make VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        Model VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        Year INT,
        EngineFuelType VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        EngineHP FLOAT,
        EngineCylinders FLOAT,
        TransmissionType VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        DrivenWheels VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        NumberOfDoors FLOAT,
        MarketCategory VARCHAR(100) COLLATE Latin1_General_100_BIN2_UTF8,
        VehicleSize VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        VehicleStyle VARCHAR(50) COLLATE Latin1_General_100_BIN2_UTF8,
        HighwayMPG INT,
        CityMPG INT,
        Popularity INT,
        MSRP FLOAT
    ) AS [result]
WHERE
    Make = 'Toyota'
ORDER BY
    Year ASC;
