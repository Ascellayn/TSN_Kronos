from TSN_Abstracter import *;
import fastapi; # pyright: ignore[reportUnusedImport]





# Due to a bug with how Kronos is deployed, App.tsna is NEVER read correctly, so we manually read it.
App.JSON(File.JSON_Read("App.tsna"));
API: fastapi.FastAPI = fastapi.FastAPI();