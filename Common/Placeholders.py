from .Globals import *;



BASE_AUTHOR: str = cast(str, File.Read("Templates/Author.txt"));
BASE_KEYWORDS: str = cast(str, File.Read("Templates/Author.txt"));

DEFAULT_BANNER: str = cast(str, File.Read("Templates/Default_Banner.txt"));
DEFAULT_COLOR: str = cast(str, File.Read("Templates/Default_Color.txt"));
DEFAULT_LANG: str = cast(str, File.Read("Templates/Default_Lang.txt"));
DEFAULT_THEME: str = cast(str, File.Read("Templates/Default_Theme.txt"));

SOURCE_CSS: str = cast(str, File.Read("Templates/Source_CSS.txt"));
SOURCE_JS: str = cast(str, File.Read("Templates/Source_JS.txt"));





def Basic_Replacement(HTML: str) -> str:
	return String.Bulk_Replace(
		[
			("{DEFAULT_BANNER}", DEFAULT_BANNER),
			("{DEFAULT_COLOR}", DEFAULT_BANNER),
			("{DEFAULT_LANG}", DEFAULT_LANG),
			("{DEFAULT_THEME}", DEFAULT_THEME),
			("{SOURCE_CSS}", SOURCE_CSS),
			("{SOURCE_JS}", SOURCE_JS),
			("{KRONOS_AppTSNA}", str(App.Dump())),
			("{KRONOS_VERSION}", f"v{'.'.join(String.ify_Array(App.Version))}"),
			("{AUTHOR_BASE}", BASE_AUTHOR),
			("{KEYWORDS_BASE}", BASE_KEYWORDS)
		], HTML
	);





def Build_Time(HTML: str, Unix_Starting: float) -> str:
	time: float = Time.Get_Unix(True) - Unix_Starting;

	App.Public["Build_Average"].append(time);
	if (len("Build_Average") > 255): App.Public["Build_Average"].pop(0);

	avg: float = sum(App.Public["Build_Average"]) / len(App.Public["Build_Average"]);

	return String.Bulk_Replace(
		[
			("{KRONOS_BUILD-TIME}", Time.Elapsed_String(time, Show_Until=-3)),
			("{KRONOS_BUILD-AVERAGE}", Time.Elapsed_String(avg, Show_Until=-3)),
			("{KRONOS_BUILD-AVERAGE_SAMPLES}", str(len(App.Public["Build_Average"]))),
		], HTML
	);