from .Globals import *;



BASE_AUTHOR: str = cast(str, File.Read("Templates/Author.txt"));
BASE_KEYWORDS: str = cast(str, File.Read("Templates/Keywords.txt"));

DEFAULT_BANNER: str = cast(str, File.Read("Templates/Default_Banner.txt"));
DEFAULT_COLOR: str = cast(str, File.Read("Templates/Default_Color.txt"));
DEFAULT_LANG: str = cast(str, File.Read("Templates/Default_Lang.txt"));
DEFAULT_THEME: str = cast(str, File.Read("Templates/Default_Theme.txt"));

SOURCE_CSS: str = cast(str, File.Read("Templates/Source_CSS.txt"));
SOURCE_JS: str = cast(str, File.Read("Templates/Source_JS.txt"));





def Base(HTML: str) -> str:
	return String.Bulk_Replace(
		[
			("{BANNER}", DEFAULT_BANNER),
			("{COLOR}", DEFAULT_COLOR),
			("{LANG}", DEFAULT_LANG),
			("{THEME}", DEFAULT_THEME),
			("{SOURCE_CSS}", SOURCE_CSS),
			("{SOURCE_JS}", SOURCE_JS),
			("{KRONOS_AppTSNA}", str(App.Dump())),
			("{KRONOS_VERSION}", f"v{'.'.join(String.ify_Array(App.Version))}"),
			("{AUTHOR}", BASE_AUTHOR),
			("{KEYWORDS_BASE}", BASE_KEYWORDS)
		], HTML
	);

def Article(HTML: str, kMD_JSON: dict[str, Any]) -> str:
	return Base(
		String.Bulk_Replace(
			[
				("{BANNER}", kMD_JSON.get("Banner", "{BANNER}")),
				("{COLOR}", kMD_JSON.get("Color", "{COLOR}")),
				("{LANG}", kMD_JSON.get("Lang", "{LANG}")),
				("{THEME}", kMD_JSON.get("Theme", "{THEME}")),
				("{AUTHOR}", kMD_JSON.get("Author", "{AUTHOR}")),
				("{KEYWORDS}", kMD_JSON.get("Keywords", "{KEYWORDS}")),
				("{TITLE}", kMD_JSON["Name"]),
				("{DESCRIPTION}", kMD_JSON["Description"]),
				("{AUTHOR}", kMD_JSON["Author"]),
				("{DATE}", " ".join(Time.Get_DateStrings(Time.Convert_ISO8601(kMD_JSON["Date"]))))
			], HTML
		)
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