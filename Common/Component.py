from .Globals import *;
import re;



HEADER: str = cast(str, File.Read("Templates/Components/Header.html"));





def Handle_Words(Article: str, kMD_Text: str) -> str:
	Words: int = len(re.findall(r"[a-zA-Z]+", kMD_Text));
	Reading: str = Time.Elapsed_String(Words / 3, Show_Until=1, Trailing_Starting=0, Display_Units_Long=True);
	# Source for 180WPM: https://en.wikipedia.org/wiki/Words_per_minute

	return String.Bulk_Replace(
		[
			("{ARTICLE_WORDS}", str(Words)),
			("{ARTICLE_LENGTH}", Reading)
		]
		, Article
	);