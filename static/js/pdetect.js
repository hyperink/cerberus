var dropIn = function(_json){
	var elem = document.createElement(_json.tag);
	if (_json.class){
		elem.setAttribute("class", _json.class);
	}
	if (_json.style){
	    elem.setAttribute("style", _json.style);
	}
	if (_json.id){
		elem.setAttribute("id", _json.id);
	}
	if (_json.CE && _json.CE === "true"){
		elem.setAttribute("contenteditable", "true");
	}
	if(_json.text){
		elem.innerHTML = _json.text;
	}
	if(_json.handler){
		elem.sendClick(_json.handler);
	}
	if (_json.self){
		_json.self(elem);
	}
	this.appendChild(elem);
}
Node.prototype.dropIn=this.dropIn;

(function(){

	var gTitles = [],
		gDIDs = [],
		tahead = $('.typeahead'),
		grabbedAllTitles = false;

	(function(){

		var credentials = "";

		var ajaxGet = function(location, callBack){
			$('ajaxloader').style.display = "block";
			var req_ = (window.XMLHttpRequest) ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
			req_.onreadystatechange=function(){
				if (req_.readyState==4 && req_.status==200){
					var data_ = req_.responseText;
					callBack(JSON.parse(data_));
				}
			}
			req_.open("GET", location, true)
			req_.send(null);
		};
		var ajaxPost = function(location, data, callBack){
			$('ajaxloader').style.display = "block";
			var req_ = (window.XMLHttpRequest) ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
			req_.onreadystatechange=function(){
				if (req_.readyState==4 && req_.status==200){
					var data_ = req_.responseText;
					callBack(JSON.parse(data_));
				}
				if (req_.readyState==4 && req_.status==500){
				    console.log("timed out, trying again");
				    ajaxPost(location, data, callBack);
				}
			}
			req_.open("POST", location, true)
			req_.send(data);
		}

		var $ = function(elem){
			return document.getElementById(elem);
		}

		// Trigger Type-ahead via Twitter Bootstrap plugin (after input data property is set for it)
		var triggerTA = function(){
			tahead.typeahead();
			$('search').onkeydown=function(e){
				if (e.keyCode === 13 && this.value.length > 10){ // ENTER/RETURN pressed
					var title = this.value, // Title entered in search bar via typeahead
						did,
						byDID = false; // By default assumes entered title/text is a URL
					for (var i=0,len=gTitles.length;i<len;i++){ // Search through the title list array to grab the associated Google Document ID needed for the API
						if (gTitles[i] === title){ // Match by title
							did = gDIDs[i]; // If match is found, grab the related DID via identical index valye in DID array
							byDID = true; // Flags the content as non-URL
						}
					}
					if (byDID === false){
						// No title match found, send title / input value through API as URL
						ajaxPost('http://ec2dev.servehttp.com:7357/check?url=' + title, '', populate)
					} else {
						// Title match found, DID grabbed and sent through API
						ajaxPost('http://ec2dev.servehttp.com:7357/check?' + credentials + '&did=' + did + '&test=1', '', populate)
					}
				}
			}
		};

		var postAuthorize = function(data){
			// Data returned is an array of objects containing title and Document ID of account's google documents
			for (var i=0,len=data.length;i<len;i++){
				gTitles.push(data[i].title);
				gDIDs.push(data[i].id);
				// These are added to two different arrays with the assumption that their array index position values will be the same
			}
			var str = JSON.stringify(gTitles);
			$('search').setAttribute('data-source', str); // Set attribute required by twitter bootstrap's TypeAhead plugin
			triggerTA();
			$('cover').style.display = "none";
			$('ajaxloader').style.display = "none";
		}

		// Posts google account login info to grant access via google docs API
		var authorize = function(){
			var _name = function(){
				var raw = $('email').value;
				if (raw.match('@hyperinkpress.com')){ // If full email address is entered, simply send full value through
					return raw;
				} else {
					return raw + "@hyperinkpress.com"; // If only prefix to email address is entered, append the suffix automatically
				}
			}
			credentials = "email=" + _name() + "&password=" + $('password').value;
			ajaxPost('http://ec2dev.servehttp.com:7357/list?' + credentials, "", postAuthorize);
		}

		// Depreciated rendering function. Collects text snippet duplicates and displays sources grouped together underneat. Problem was that it prunes the text and maintains only the first found original.
		var _populate = function(data){
			var str = "",
				snippetStr = "",
				checker = [],
				renderArr = [];
			$('scoreContainer').style.display='block';
			for (var i=0,len=data.data.result.length;i<len;i++){
				var titleLink = '<a href="' + data.data.result[i].url + '" target="_blank">' + data.data.result[i].title + '</a>',
					urlLink = '<a class="sourceURL" target="_blank" href="' + data.data.result[i].url + '">' + String(data.data.result[i].url).replace('http://',"").replace('https://',"").replace('www.',"") + '</a>',
					txt = '<div><span class="section">' + data.data.result[i].htmlsnippet + '</span>';
				var indx = -1;
				for (var k=0,Len=checker.length;k<Len;k++){
					if (txt.substring(28,100) === checker[k].substring(28,100)){
						indx = k;
					}
				}
				if (indx < 0){
					checker.push(txt);
					renderArr.push({
						indx : (checker.length - 1),
						txt : txt,
						sources : urlLink
					})
				} else {
					for (var j=0,_len=renderArr.length;j<_len;j++){
						if (renderArr[j].indx === indx) renderArr[j].sources += urlLink
					}
				}
				str += titleLink;
			}
			for (var i=0,len=renderArr.length;i<len;i++){
				snippetStr += renderArr[i].txt + renderArr[i].sources + '</div>';
			}
			$('urlsWrapper').innerHTML = str;
			$('scoreCard').innerHTML = snippetStr;
			$('score').innerHTML = Math.round(((data.metric * 5) / Math.PI) * 10000) / 100;
			$('scoreContainer').style.display = "block";
			$('scoreList').style.display = "none";
			$('ajaxloader').style.display = "none";
		}

		$('submitBtn').onclick=authorize;
		$('password').onkeydown=function(e){
			if (e.keyCode === 13){
				authorize();
			}
		}

		var populate = function(data){
			var UrlsStr = "", // Stores side bar's list of URLs
				contentStr = "", // Stores the right content area's full HTML contents as a string to reduce rendering time (potentially large amount of data)
				resArr = []; // Keep track of each result so that they can be sorted by match % before being added to contentStr for HTML injection
			$('scoreContainer').style.display='block';
			for (var i=0,len=data.data.result.length;i<len;i++){
				var titleLink = '<a href="' + data.data.result[i].url + '" target="_blank">' + data.data.result[i].title + '</a>',
					txt = '<div><span class="section">' + data.data.result[i].htmlsnippet + '</span>',
					urlLink = '<a class="sourceURL" target="_blank" href="' + data.data.result[i].url + '">' + String(data.data.result[i].url).replace('http://',"").replace('https://',"").replace('www.',"") + '</a>';
				UrlsStr += titleLink;
				var obj = {};
				// Sometimes the needed keys for calculating the % match per result do not exist. If they do, it's matched words / total words; otherwise, 0 (for array sorting purposes)
				obj.match = (data.data.result[i].wordsmatched && data.data.result[i].urlwords) ? parseInt(data.data.result[i].wordsmatched[0]) / parseInt(data.data.result[i].urlwords[0]) * 100 : 0;
				obj.snippet = (txt + urlLink);
				resArr.push(obj)
			}
			resArr.sort(function(a,b){return b.match - a.match}) // Sort the results by highest to lowest % match pre-rendering
			for (var i=0,len=resArr.length;i<len;i++){
				// Builds the content-injection string with results sorted by match %
				contentStr += ('<br/><span class="matchPer" style="width:' + ((resArr[i].match !== 0) ? (resArr[i].match * 0.9) + '%' : 'auto;opacity:0.25') + '">' + ((resArr[i].match !== 0) ? Math.round(resArr[i].match) + "%" : 'N/A') + '</span>' + resArr[i].snippet)
			}
			// Goofy time!
			$('urlsWrapper').innerHTML = UrlsStr;
			$('scoreCard').innerHTML = contentStr;
			$('score').innerHTML = Math.round(((data.metric * 5) / Math.PI) * 10000) / 100;
			$('scoreContainer').style.display = "block";
			$('scoreList').style.display = "none";
			$('ajaxloader').style.display = "none";
		}

		// If the List option is selected for viewing a full list of results, render and display them
		var grabListedTitle = function(){
			grabbedAllTitles = true; // Flags the list as rendered and grabbed so that this function is only run once
			var list = $('scoreList');
			$('scoreContainer').style.display='none';
			list.style.display='block;'
			ajaxGet('http://ec2dev.servehttp.com:7357/copywrong', function(data){
				data.sort(function(a,b){return b.score - a.score}); // Sorts the list results from CouchDB by highest to lowest plagiarism probability score
				setTimeout(function(){ // It's a big list to sort and JS sometimes chokes in some bizarre asynchronous behavior, so we give a generous extra half second before rendering
					for (var i=0,len=data.length;i<len;i++){
						var score = Math.round(((data[i].score * 5) / Math.PI) * 10000) / 100; // Adjust score to readable % out of 100
						if (data[i].score === null) score = "N/A"; // Some data unavailable, N/A it
						list.dropIn({ // Add the list container
							tag: "div",
							class : "sRow",
							self : function(wrapper){
								wrapper.wpid = data[i].wpid;
								wrapper._title = data[i].title;
								wrapper.dropIn({ // Add the list title, which links to the book
									tag: "a",
									class : "lTitles",
									text : data[i].title,
									self : function(elem){
										elem.setAttribute("target","_blank");
										elem.setAttribute("href", "http://www.hyperinkpress.com/" + data[i].slug + "/print-ebook.php?token=typosaurus")
									}
								});
								wrapper.dropIn({ // Add the book's score on the right, which pops up a new tab/window with the analysis details for that book
									tag: "a",
									class : "rScores floatRight",
									text : score,
									self : function(elem){
										elem.setAttribute('href','#'+ wrapper.wpid + '&' + wrapper._title);
										elem.setAttribute('target','_blank');
									}
								});
							}
						})
					}
				}, 500)
				$('ajaxloader').style.display = "none";
			})
		}

		// Function for skipping google docs login. Simply hide the blocking elements
		var showListOnly = function(){
			$('scoreContainer').style.display='none';
			$('cover').style.display='none';
			$('scoreList').style.display='block';
			if (grabbedAllTitles === false) grabListedTitle(); // Only render the list if it hasn't been rendered already (false by default)
		}

		$('listTrigger').onclick=showListOnly; // Clicking "List" from top bar near input field
		$('skiplogin').onclick=showListOnly; // Clicking the link to skip login at load

		// Automatically render the details for a given book if the URL contains either that book's title or another URL
		if (window.location.hash){
			var info = window.location.hash.split('&'),
				wpid = info[0].substring(1,info[0].length),
				title = info[1];
			$('cover').style.display='none';
			$('scoreList').style.display='none';
			if (!window.location.hash.match('http')){ // HTTP or HTTPS address is inputed instead of title, for simple checking against copyscape api via our UI
				$('scoreContainer').style.display='block';
				ajaxGet('http://ec2dev.servehttp.com:7357/copywrong/' + wpid + '?data=true', function(d){
					populate(d[0].data); // Render detail view
					$('search').value = title; // Sets title in input field, simply for display purposes (to know what book we're reviewing)
				})
			} else {
				// URL goes through copyscape API via our backend
				ajaxPost('http://ec2dev.servehttp.com:7357/check?url=' + window.location.hash.substring(1,window.location.hash.length), '', populate)
			}
		}

	})()

})()