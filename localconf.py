import web

PRINT_EBOOK_TOKEN = "typosaurus"
MARKETPLACE_HOST = "marketplace.cxafnm9ktly7.us-west-1.rds.amazonaws.com" 
MARKETPLACE_DB = 'wordpress'
MARKETPLACE_USR = 'awsroot'
MARKETPLACE_PWD =  'uOyrr1jWpSvP1gaJLaar'
mpdb = web.database(host=MARKETPLACE_HOST, dbn='mysql', db=MARKETPLACE_DB, user=MARKETPLACE_USR, pw=MARKETPLACE_PWD)

DEFAULT = """{"metric": 0.008659933728144387, "data": {"count": ["6"], "querywords": ["6304"], "result": [{"textmatched": ["is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy ... impossible to say exactly what ... watching, and impossible to pull your eyes away"], "index": ["1"], "minwordsmatched": ["38"], "title": ["RS_Louie_CK_Jonah_Weiner"], "url": ["http://jonahweiner.com/RS_Louie_CK_Jonah_Weiner.html"], "urlwords": ["3742"], "htmlsnippet": ["<font color=\"#777777\">... Louie </font><font color=\"#000000\">is a  ... Louie is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy: </font><font color=\"#777777\">It\u2019s </font><font color=\"#000000\">impossible to say exactly what </font><font color=\"#777777\">you\u2019re </font><font color=\"#000000\">watching, and impossible to pull your eyes away. ... </font>"], "wordsmatched": ["34"], "textsnippet": ["... Louie is a  ... Louie is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy: It\u2019s impossible to say exactly what you\u2019re watching, and impossible to pull your eyes away. ... "]}, {"textmatched": ["is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy ... impossible to say exactly what ... watching, and impossible to pull your eyes away"], "index": ["2"], "minwordsmatched": ["38"], "title": ["How Louis C.K. Became the Darkest, Funniest Comedian in ..."], "url": ["http://www.rollingstone.com/movies/news/how-louis-c-k-became-the-darkest-funniest-comedian-in-america-20111212"], "urlwords": ["1325"], "htmlsnippet": ["<font color=\"#777777\">... Louie </font><font color=\"#000000\">is a  ... Louie is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy: </font><font color=\"#777777\">It's </font><font color=\"#000000\">impossible to say exactly what </font><font color=\"#777777\">you're </font><font color=\"#000000\">watching, and impossible to pull your eyes away. ... </font>"], "wordsmatched": ["34"], "textsnippet": ["... Louie is a  ... Louie is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy: It's impossible to say exactly what you're watching, and impossible to pull your eyes away. ... "]}, {"textmatched": ["is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy ... impossible to say exactly what ... watching, and impossible to pull your eyes away"], "index": ["3"], "minwordsmatched": ["34"], "title": ["Rolling Stone Mobile - News - Movies: How Louis C.K. Became ..."], "url": ["http://m.rollingstone.com/?redirurl=/movies/news/how-louis-c-k-became-the-darkest-funniest-comedian-in-america-20111212"], "urlwords": ["846"], "htmlsnippet": ["<font color=\"#777777\">... Louie </font><font color=\"#000000\">is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy: </font><font color=\"#777777\">It's </font><font color=\"#000000\">impossible to say exactly what </font><font color=\"#777777\">you're </font><font color=\"#000000\">watching, and impossible to pull your eyes away. ... </font>"], "wordsmatched": ["34"], "textsnippet": ["... Louie is a critically adored hit that blurs together cringe comedy, poignant drama, bathroom humor, slapstick gore and surrealist flights of fancy: It's impossible to say exactly what you're watching, and impossible to pull your eyes away. ... "]}, {"index": ["4"], "minwordsmatched": ["28"], "title": ["www.toptenmba.org"], "url": ["http://www.toptenmba.org/files/2011/08/GMAT-Prep1.pdf"], "htmlsnippet": ["<font color=\"#777777\">... </font><font color=\"#000000\">We do not take responsibility for any misfortune that may happen, either directly or indirectly, from reading and applying the information contained and/or referenced in this ebook. ... </font>"], "textsnippet": ["... We do not take responsibility for any misfortune that may happen, either directly or indirectly, from reading and applying the information contained and/or referenced in this ebook. ... "]}, {"index": ["5"], "minwordsmatched": ["28"], "title": ["Biography On Louis CK"], "url": ["http://www.hyperink.com/Biography-On-Louis-Ck-b749"], "htmlsnippet": ["<font color=\"#777777\">... </font><font color=\"#000000\">And crude he often is with jokes that talk about masturbation, farts, sucking dicks,   and even gay marriage. In his fans' opinion, however, Louis' shock value is just ... </font>"], "textsnippet": ["... And crude he often is with jokes that talk about masturbation, farts, sucking dicks,   and even gay marriage. In his fans' opinion, however, Louis' shock value is just ... "]}, {"index": ["6"], "minwordsmatched": ["16"], "title": ["Tanning tips and fake tanning."], "url": ["http://www.art-seekers.com/tanning.php"], "htmlsnippet": ["<font color=\"#777777\">... </font><font color=\"#000000\">We do not </font><font color=\"#777777\">accept any </font><font color=\"#000000\">responsibility for any </font><font color=\"#777777\">anything </font><font color=\"#000000\">that may happen either directly or indirectly </font><font color=\"#777777\">as a result of reading or using </font><font color=\"#000000\">the information contained </font><font color=\"#777777\">on this page. ... </font>"], "textsnippet": ["... We do not accept any responsibility for any anything that may happen either directly or indirectly as a result of reading or using the information contained on this page. ... "]}]}}"""