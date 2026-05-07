from Common import *;





@API.get("/articles", response_class=fastapi.responses.HTMLResponse)
def HTML_FrontPage():
	build_init: float = Time.Get_Unix(True);
	HTML: str = Placeholders.Base(cast(str, File.Read("Templates/Page/Front.html")));
	return Placeholders.Build_Time(HTML, build_init);





@API.get("/article/test", response_class=fastapi.responses.HTMLResponse)
def HTML_Test():
	build_init: float = Time.Get_Unix(True);

	try: HTML: str = Article.Process("Articles/Test.md");
	except Exception as E: return HTML_Error(E);

	return Placeholders.Build_Time(HTML, build_init);