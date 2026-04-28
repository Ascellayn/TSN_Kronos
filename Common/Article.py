from .Globals import *;
from . import Component; # pyright: ignore[reportUnusedImport]
from . import MarkTSN;
from . import Placeholders;



TEMPLATE: str = cast(str, File.Read("Templates/Page/Article.html"));



def Process(P: str) -> str:
	if (not File.Exists(P)): raise Exception(f"Article at {P} does not exist.");

	kmd_raw: str = cast(str, File.Read(P));
	if ("=¤=" not in kmd_raw): raise Exception(f"Invalid Kronos Markdown");


	kmd_split: list[str] = kmd_raw.split("=¤=", 1);
	del kmd_raw;

	try:
		kMD_JSON: dict[str, Any] = json.loads(kmd_split[0]);
		kMD_Text: str = kmd_split[1];
		del kmd_split;
	except Exception as E: raise Exception(f"Invalid Kronos Article: {str(E)}");

	Article: str = TEMPLATE;
	Article = Article.replace("{ARTICLE_HEADER}", Component.HEADER);
	Article = Component.Handle_Words(Article, kMD_Text);
	Article = Article.replace("{ARTICLE_HTML}", MarkTSN.toHTML(kMD_Text));

	return Placeholders.Article(Article, kMD_JSON);