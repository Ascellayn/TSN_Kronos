# TODO: Dashlists are annoying as fu-
from .Globals import *;
import re;



H6: re.Pattern[str] = re.compile(r"(?<=^###### ).+", flags=re.MULTILINE);
H5: re.Pattern[str] = re.compile(r"(?<=^##### ).+", flags=re.MULTILINE);
H4: re.Pattern[str] = re.compile(r"(?<=^#### ).+", flags=re.MULTILINE);
H3: re.Pattern[str] = re.compile(r"(?<=^### ).+", flags=re.MULTILINE);
H2: re.Pattern[str] = re.compile(r"(?<=^## ).+", flags=re.MULTILINE);
H1: re.Pattern[str] = re.compile(r"(?<=^# ).+", flags=re.MULTILINE);

BOLD: re.Pattern[str] = re.compile(r"(?<=\*\*).+(?=\*\*)", flags=re.MULTILINE);
ITALIC: re.Pattern[str] = re.compile(r"(?<=\*).+(?=\*)", flags=re.MULTILINE);
UNDERLINE: re.Pattern[str] = re.compile(r"(?<=__).+(?=__)", flags=re.MULTILINE);

CODEBLOCK: re.Pattern[str] = re.compile(r"(?<=```)(\w+)?[^`]+(?=```)", flags=re.MULTILINE); # First line should be equal to group
CODE: re.Pattern[str] = re.compile(r"(?<=`)[^`]+(?=`)", flags=re.MULTILINE);

QUOTEBLOCK: re.Pattern[str] = re.compile(r"(?<=^>>>)(\w+)?[^<]+(?=<<<)", flags=re.MULTILINE); # First line should be equal to SNC-Color
QUOTE: re.Pattern[str] = re.compile(r"(?<=^>)(\w+)?[^\n]+", flags=re.MULTILINE);

IMAGE: re.Pattern[str] = re.compile(r"!\[(.+)\]\((.+)\)", flags=re.MULTILINE);
LINK: re.Pattern[str] = re.compile(r"\[(.+)\]\((.+)\)", flags=re.MULTILINE);



R_H6: re.Pattern[str] = re.compile(r"^###### .+", flags=re.MULTILINE);
R_H5: re.Pattern[str] = re.compile(r"^##### .+", flags=re.MULTILINE);
R_H4: re.Pattern[str] = re.compile(r"^#### .+", flags=re.MULTILINE);
R_H3: re.Pattern[str] = re.compile(r"^### .+", flags=re.MULTILINE);
R_H2: re.Pattern[str] = re.compile(r"^## .+", flags=re.MULTILINE);
R_H1: re.Pattern[str] = re.compile(r"^# .+", flags=re.MULTILINE);

R_BOLD: re.Pattern[str] = re.compile(r"\*\*.+\*\*", flags=re.MULTILINE);
R_ITALIC: re.Pattern[str] = re.compile(r"\*.+\*", flags=re.MULTILINE);
R_UNDERLINE: re.Pattern[str] = re.compile(r"__.+__", flags=re.MULTILINE);

R_CODEBLOCK: re.Pattern[str] = re.compile(r"```(\w+)?[^`]+```", flags=re.MULTILINE);
R_CODE: re.Pattern[str] = re.compile(r"`[^`]+`", flags=re.MULTILINE);

R_QUOTEBLOCK: re.Pattern[str] = re.compile(r"^>>>(\w+)?[^<]+<<<", flags=re.MULTILINE);
R_QUOTE: re.Pattern[str] = re.compile(r"^>(\w+)?[^\n]+", flags=re.MULTILINE);





C_CODEBLOCK: str = cast(str, File.Read("Templates/Components/Codeblock.html"));
C_QUOTEBLOCK: str = cast(str, File.Read("Templates/Components/Quoteblock.html"));
C_QUOTE: str = cast(str, File.Read("Templates/Components/Quote.html"));

C_IMAGE: str = cast(str, File.Read("Templates/Components/Image.html"));
C_LINK: str = cast(str, File.Read("Templates/Components/Link.html"));





def __Mark_Tagger(R_Regex: re.Pattern[str], Regex: re.Pattern[str], Md: str, Tag: str) -> str:
	regex_pairs: list[tuple[str, str]] = [];
	for r_m in R_Regex.finditer(Md):
		for m in Regex.finditer(Md[r_m.start() : r_m.end()]):
			regex_pairs.append((Md[r_m.start() : r_m.end()], f"<{Tag}>{Md[r_m.start() : r_m.end()][m.start() : m.end()]}</{Tag}>"));
			break; # ← Failsafe, supposed to happen only once anyways. Inside of an finditer because of Regex weirdness
	return String.Bulk_Replace(regex_pairs, Md); # pyright: ignore[reportArgumentType] // TBD: TSNA v6.1.2 needs to fix typing here



def __Mark_Tagger_Block(R_Regex: re.Pattern[str], Regex: re.Pattern[str], Md: str, Template: str) -> str:
	regex_pairs: list[tuple[str, str]] = [];
	for r_m in R_Regex.finditer(Md):
		for m in Regex.finditer(Md[r_m.start() : r_m.end()]):
			regex_pairs.append(
				(
					Md[r_m.start() : r_m.end()],
					String.Bulk_Replace([
						("{ATTRIBUTE}", str(r_m.group(1))),
						("{CONTENT}", Md[r_m.start() : r_m.end()][m.start() : m.end()]\
.replace(str(r_m.group(1)) if (r_m.group(1)) else "", "", 1)\
.replace("{ATTRIBUTE}", str(r_m.group(1))))
					], Template)
				) # Ogata gonna be mad as fuuuuuuuuck
			);
			break; # ← Failsafe, supposed to happen only once anyways. Inside of an finditer because of Regex weirdness
	return String.Bulk_Replace(regex_pairs, Md); # pyright: ignore[reportArgumentType] // TBD: TSNA v6.1.2 needs to fix typing here



def __Mark_Tagger_Pair(Regex: re.Pattern[str], Md: str, Template: str, Reverse: bool = False) -> str:
	regex_pairs: list[tuple[str, str]] = [];
	for m in Regex.finditer(Md):
		regex_pairs.append((
			m.group(0),
			String.Bulk_Replace(
				[
					("{CONTENT}", m.group(1 if (Reverse) else 2)),
					("{ATTRIBUTE}", m.group(2 if (Reverse) else 1))
				],
				Template
			)
		));
	return String.Bulk_Replace(regex_pairs, Md); # pyright: ignore[reportArgumentType] // TBD: TSNA v6.1.2 needs to fix typing here





def toHTML(Md: str) -> str:
	# Block Components
	Md = __Mark_Tagger_Block(R_CODEBLOCK, CODEBLOCK, Md, C_CODEBLOCK);
	Md = __Mark_Tagger_Block(R_QUOTEBLOCK, QUOTEBLOCK, Md, C_QUOTEBLOCK);
	Md = __Mark_Tagger_Block(R_QUOTE, QUOTE, Md, C_QUOTE);


	# Headers
	Md = __Mark_Tagger(R_H6, H6, Md, "h6");
	Md = __Mark_Tagger(R_H5, H5, Md, "h5");
	Md = __Mark_Tagger(R_H4, H4, Md, "h4");
	Md = __Mark_Tagger(R_H3, H3, Md, "h3");
	Md = __Mark_Tagger(R_H2, H2, Md, "h2");
	Md = __Mark_Tagger(R_H1, H1, Md, "h1");


	# Paragraph everything else
	md: list[str] = Md.split("\n");
	for i, l in enumerate(Md.split("\n")):
		if (l.strip() == ""): md[i] = ""; continue;
		if (l.strip().startswith("<")): continue;
		md[i] = f"{l.replace(l.strip(), "")}<p>{l.strip()}</p>";

	while ("" in md): md.remove("");
	Md = "\n".join(md);


	# Populate Text
	Md = __Mark_Tagger(R_BOLD, BOLD, Md, "b");
	Md = __Mark_Tagger(R_ITALIC, ITALIC, Md, "i");
	Md = __Mark_Tagger(R_UNDERLINE, UNDERLINE, Md, "u");
	Md = __Mark_Tagger(R_CODE, CODE, Md, "c");

	Md = __Mark_Tagger_Pair(IMAGE, Md, C_IMAGE);
	Md = __Mark_Tagger_Pair(LINK, Md, C_LINK, True);

	print(Md);
	return Md;