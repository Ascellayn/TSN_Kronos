from Common import *;





@API.get("/articles", response_class=fastapi.responses.HTMLResponse)
def HTML_FrontPage():
	build_init: float = Time.Get_Unix(True);
	HTML: str = Placeholders.Basic_Replacement(cast(str, File.Read("Templates/Page/Front.html")));
	return Placeholders.Build_Time(HTML, build_init);